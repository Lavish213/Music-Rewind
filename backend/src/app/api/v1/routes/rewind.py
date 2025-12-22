from fastapi import APIRouter

router = APIRouter(prefix="/rewind", tags=["rewind"])


@router.get("/summary")
def rewind_summary():
    return {
        "user": {"name": "Demo User"},
        "topArtist": "Kendrick Lamar",
        "topSong": "HUMBLE.",
        "minutesPlayed": 12345,
    }