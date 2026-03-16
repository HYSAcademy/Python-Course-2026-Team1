import zipfile
import os
from typing import List, Dict, Any


class ArchiveProcessor:
    @staticmethod
    def process_archive(file_path: str) -> Dict[str, Any]:
        """
        Extracts metadata and text content from all files inside the ZIP.
        """
        files_data = []
        total_size = os.path.getsize(file_path)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.is_dir():
                    with zip_ref.open(file_info.filename) as f:
                        try:
                            content = f.read().decode('utf-8')
                        except UnicodeDecodeError:
                            content = "[Binary or non-UTF8 content]"

                    files_data.append({
                        "path": file_info.filename,
                        "size": file_info.file_size,
                        "extension": os.path.splitext(file_info.filename)[1],
                        "content": content
                    })

        return {
            "filename": os.path.basename(file_path),
            "file_size": total_size,
            "files_count": len(files_data),
            "files": files_data
        }