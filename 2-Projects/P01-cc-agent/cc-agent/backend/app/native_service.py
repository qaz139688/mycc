import subprocess
import asyncio
from typing import Optional, List
from datetime import datetime
import uuid
import os
import logging

from app.models import (
    NativeCommandRequest, NativeCommandResponse, NativeCommandLog,
    FileOperationRequest, FileOperationResponse
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "native_logs")

def ensure_logs_dir():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

def _run_command_sync(command: str, shell_type: str, timeout: int) -> tuple:
    if shell_type == 'cmd':
        result = subprocess.run(
            ['cmd', '/c', command],
            capture_output=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    elif shell_type == 'powershell':
        result = subprocess.run(
            ['powershell', '-NoProfile', '-NonInteractive', '-Command', command],
            capture_output=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    else:
        raise ValueError(f"Unsupported shell type: {shell_type}")
    
    return result.stdout, result.stderr, result.returncode

def _decode_output(data: bytes) -> str:
    if not data:
        return ""
    for encoding in ['utf-8', 'gbk', 'cp936', 'latin-1']:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode('utf-8', errors='replace')

async def execute_native_command(request: NativeCommandRequest) -> NativeCommandResponse:
    ensure_logs_dir()
    
    command = request.command
    shell_type = request.shell_type
    timeout = request.timeout or 30
    
    log_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"Executing command: {command} with shell: {shell_type}")
    
    stdout = b""
    stderr = b""
    return_code = -1
    
    try:
        stdout, stderr, return_code = await asyncio.to_thread(
            _run_command_sync, command, shell_type, timeout
        )
        logger.info(f"Process completed. stdout: {stdout}, stderr: {stderr}, returncode: {return_code}")
        
    except subprocess.TimeoutExpired:
        stderr = b"Command timed out"
        logger.warning(f"Command timed out after {timeout} seconds")
    except Exception as e:
        import traceback
        logger.error(f"Exception executing command: {e}")
        logger.error(traceback.format_exc())
        stderr = str(e).encode() if str(e) else b"Unknown error"
    
    output = _decode_output(stdout.strip() if stdout else b"")
    error_msg = _decode_output(stderr.strip() if stderr else b"") or None
    
    duration = (datetime.now() - start_time).total_seconds()
    
    success = return_code == 0
    
    log_entry = NativeCommandLog(
        id=log_id,
        command=command,
        shell_type=shell_type,
        output=output,
        error=error_msg,
        exit_code=return_code,
        timestamp=start_time,
        duration=duration
    )
    
    save_log(log_entry)
    
    return NativeCommandResponse(
        success=success,
        output=output,
        error=error_msg,
        exit_code=return_code
    )

async def execute_file_operation(request: FileOperationRequest) -> FileOperationResponse:
    operation = request.operation
    path = request.path
    content = request.content
    encoding = request.encoding or 'utf-8'
    
    logger.info(f"File operation: {operation} on {path}, content={repr(content)}")
    
    try:
        if operation == 'read':
            if not os.path.exists(path):
                return FileOperationResponse(
                    success=False,
                    error=f"File not found: {path}"
                )
            if os.path.isdir(path):
                return FileOperationResponse(
                    success=False,
                    error=f"Path is a directory, not a file: {path}"
                )
            
            with open(path, 'r', encoding=encoding) as f:
                file_content = f.read()
            
            logger.info(f"Read file: {path}, length: {len(file_content)}")
            return FileOperationResponse(
                success=True,
                content=file_content
            )
        
        elif operation == 'write':
            if content is None:
                return FileOperationResponse(
                    success=False,
                    error="Content is required for write operation"
                )
            
            dir_path = os.path.dirname(path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            
            processed_content = content.replace('\\n', '\n').replace('\\t', '\t')
            
            with open(path, 'w', encoding=encoding) as f:
                f.write(processed_content)
            
            logger.info(f"Wrote file: {path}, length: {len(processed_content)}")
            return FileOperationResponse(success=True)
        
        elif operation == 'append':
            if content is None:
                return FileOperationResponse(
                    success=False,
                    error="Content is required for append operation"
                )
            
            if not os.path.exists(path):
                return FileOperationResponse(
                    success=False,
                    error=f"File not found: {path}"
                )
            
            processed_content = content.replace('\\n', '\n').replace('\\t', '\t')
            
            with open(path, 'a', encoding=encoding) as f:
                f.write(processed_content)
            
            logger.info(f"Appended to file: {path}, length: {len(processed_content)}")
            return FileOperationResponse(success=True)
        
        elif operation == 'delete':
            if not os.path.exists(path):
                return FileOperationResponse(
                    success=False,
                    error=f"Path not found: {path}"
                )
            
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
                logger.info(f"Deleted directory: {path}")
            else:
                os.remove(path)
                logger.info(f"Deleted file: {path}")
            
            return FileOperationResponse(success=True)
        
        elif operation == 'list':
            if not os.path.exists(path):
                return FileOperationResponse(
                    success=False,
                    error=f"Path not found: {path}"
                )
            
            if not os.path.isdir(path):
                return FileOperationResponse(
                    success=False,
                    error=f"Path is not a directory: {path}"
                )
            
            files = os.listdir(path)
            logger.info(f"Listed directory: {path}, count: {len(files)}")
            return FileOperationResponse(
                success=True,
                files=files
            )
        
        elif operation == 'exists':
            exists = os.path.exists(path)
            logger.info(f"Checked existence: {path} -> {exists}")
            return FileOperationResponse(
                success=True,
                exists=exists
            )
        
        elif operation == 'edit':
            if not os.path.exists(path):
                return FileOperationResponse(
                    success=False,
                    error=f"File not found: {path}"
                )
            
            if line_number is None:
                return FileOperationResponse(
                    success=False,
                    error="line_number is required for edit operation"
                )
            
            if content is None:
                return FileOperationResponse(
                    success=False,
                    error="content is required for edit operation"
                )
            
            with open(path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            
            if line_number < 1 or line_number > len(lines):
                return FileOperationResponse(
                    success=False,
                    error=f"Invalid line number: {line_number}. File has {len(lines)} lines."
                )
            
            processed_content = content.replace('\\n', '\n').replace('\\t', '\t')
            if not processed_content.endswith('\n') and lines[line_number - 1].endswith('\n'):
                processed_content += '\n'
            
            lines[line_number - 1] = processed_content
            
            with open(path, 'w', encoding=encoding) as f:
                f.writelines(lines)
            
            logger.info(f"Edited line {line_number} in file: {path}")
            return FileOperationResponse(success=True)
        
        elif operation == 'replace':
            if not os.path.exists(path):
                return FileOperationResponse(
                    success=False,
                    error=f"File not found: {path}"
                )
            
            if old_text is None:
                return FileOperationResponse(
                    success=False,
                    error="old_text is required for replace operation"
                )
            
            if new_text is None:
                return FileOperationResponse(
                    success=False,
                    error="new_text is required for replace operation"
                )
            
            with open(path, 'r', encoding=encoding) as f:
                content_data = f.read()
            
            if old_text not in content_data:
                return FileOperationResponse(
                    success=False,
                    error=f"Text not found in file: {old_text[:50]}..."
                )
            
            new_content = content_data.replace(old_text, new_text)
            
            with open(path, 'w', encoding=encoding) as f:
                f.write(new_content)
            
            logger.info(f"Replaced text in file: {path}")
            return FileOperationResponse(success=True)
        
        else:
            return FileOperationResponse(
                success=False,
                error=f"Unknown operation: {operation}"
            )
    
    except Exception as e:
        import traceback
        logger.error(f"File operation error: {e}")
        logger.error(traceback.format_exc())
        return FileOperationResponse(
            success=False,
            error=str(e)
        )

def save_log(log_entry: NativeCommandLog):
    log_file = os.path.join(LOGS_DIR, f"{log_entry.timestamp.strftime('%Y%m%d')}.jsonl")
    
    logs = []
    if os.path.exists(log_file):
        try:
            import json
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except Exception:
            pass
    
    logs.append(log_entry.model_dump(mode='json'))
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved log: {log_entry.id}")

def get_logs(limit: int = 100) -> list[NativeCommandLog]:
    log_file = os.path.join(LOGS_DIR, f"{datetime.now().strftime('%Y%m%d')}.jsonl")
    
    if not os.path.exists(log_file):
        return []
    
    try:
        import json
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except Exception:
        return []
    
    return sorted(logs, key=lambda x: x.timestamp, reverse=True)[:limit]

def clear_logs():
    if os.path.exists(LOGS_DIR):
        for filename in os.listdir(LOGS_DIR):
            if filename.endswith('.jsonl'):
                os.remove(os.path.join(LOGS_DIR, filename))
    logger.info("Cleared all logs")
