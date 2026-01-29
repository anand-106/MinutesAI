from typing import List
from app.db.models import Dialogue


def dialouges_to_rich_text(dialoges:List[Dialogue]) -> str:
    
    dialouges_text = [
        f"""
        Speaker : {dlg.speaker}\n
        from {dlg.start_time} seconds to {dlg.end_time} seconds.\n
        Dialouge : "{dlg.text}"
        """ for dlg in dialoges
    ]

    return "\n\n".join(dialouges_text)

