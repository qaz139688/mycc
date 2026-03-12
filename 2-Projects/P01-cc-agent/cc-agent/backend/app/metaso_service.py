import httpx
import logging
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

METASO_API_URL = "https://metaso.cn/api/v1/search"

async def search_metaso(
    api_key: str,
    query: str,
    scope: str = "webpage",
    include_summary: bool = True,
    size: int = 10,
    include_raw_content: bool = False
) -> Optional[Dict[str, Any]]:
    if not api_key:
        logger.warning("Metaso API key not configured")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "scope": scope,
        "includeSummary": include_summary,
        "size": str(size),
        "includeRawContent": include_raw_content,
        "conciseSnippet": True
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.info(f"Metaso API request: URL={METASO_API_URL}, query={query}")
            response = await client.post(
                METASO_API_URL,
                headers=headers,
                json=payload
            )
            logger.info(f"Metaso API response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.info(f"Metaso API response data keys: {data.keys() if isinstance(data, dict) else 'not dict'}")
            return data
    except httpx.HTTPStatusError as e:
        logger.error(f"Metaso API HTTP error: {e}, response body: {e.response.text if hasattr(e, 'response') else 'no response'}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Metaso API request error: {e}, type: {type(e).__name__}")
        return None
    except Exception as e:
        logger.error(f"Metaso search error: {e}, type: {type(e).__name__}")
        return None
