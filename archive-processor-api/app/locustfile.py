import os
from pathlib import Path
from locust import HttpUser, task, between

BASE_DIR = Path(__file__).resolve().parent.parent
zip_path = BASE_DIR / "data" / "uploads" / "test.zip"

class ArchiveUser(HttpUser):
    # Simulate a user thinking for 1-2 seconds between actions
    wait_time = between(1, 2)

    def on_start(self):
        """Perform an initial upload to get a working archive_id."""
        with open(zip_path, "rb") as f:
            files = {"files": ("test.zip", f, "application/zip")}
            response = self.client.post("/api/v1/upload-archives/", files=files)
            if response.status_code == 200:
                data = response.json()
                self.archive_id = data["queued_archives"][0]["archive_id"]
                self._trigger_indexing()
            else:
                self.archive_id = None

    def _trigger_indexing(self):
        """Internal helper to ensure the index exists."""
        if self.archive_id:
            self.client.post(
                "/api/v1/archives/trigger", json={"archive_id": self.archive_id}
            )

    @task(10)
    def search_fox(self):
        """Frequent search requests (The primary load)."""
        if self.archive_id:
            self.client.get(
                f"/api/v1/search/{self.archive_id}?query=fox&limit=10",
                name="/api/v1/search/[id]",
            )

@task(1)
def check_status(self):
    """Occasional status checks."""
    if self.archive_id:
        # Changed 'archives' to 'status' to match your Swagger output
        self.client.get(
            f"/api/v1/status/{self.archive_id}/status",
            name="/api/v1/status/[id]/status",
        )