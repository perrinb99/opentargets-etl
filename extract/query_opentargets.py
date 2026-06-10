# extract/query_opentargets.py

import requests
import json
import os
from config import GRAPHQL_URL, DISEASE_ID, RAW_OUTPUT_PATH, PAGE_SIZE

QUERY = """
query DiseaseAssociations($diseaseId: String!, $size: Int!) {
  disease(efoId: $diseaseId) {
    id
    name
    associatedTargets(page: { index: 0, size: $size }) {
      count
      rows {
        target {
          id
          approvedSymbol
          approvedName
          biotype
        }
        score
      }
    }
  }
}
"""

def fetch_disease_associations(disease_id: str = DISEASE_ID, size: int = PAGE_SIZE) -> dict:
    """
    Fetch target associations for a given disease from Open Targets Platform.
    Returns raw API response as a dict.
    """
    payload = {
        "query": QUERY,
        "variables": {"diseaseId": disease_id, "size": size}
    }

    response = requests.post(
        GRAPHQL_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()


def save_raw(data: dict, output_path: str = RAW_OUTPUT_PATH) -> None:
    """Persist raw API response to disk for auditability."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Raw data saved to {output_path}")


if __name__ == "__main__":
    print(f"Fetching associations for disease: {DISEASE_ID}")
    data = fetch_disease_associations()
    save_raw(data)
    count = data["data"]["disease"]["associatedTargets"]["count"]
    print(f"Total associations available: {count}")
    print(f"Fetched: {len(data['data']['disease']['associatedTargets']['rows'])} rows")