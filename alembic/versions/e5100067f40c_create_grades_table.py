"""Create Grades table

Revision ID: e5100067f40c
Revises: 
Create Date: 2025-08-11 02:40:24.888453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5100067f40c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "grades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "enrollment_id",
            sa.Integer(),
            sa.ForeignKey("enrollments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("grade", sa.String(length=2), nullable=True),
        sa.Column("graded_on", sa.Date(), nullable=True),
    )
    op.create_index("ix_grades_enrollment_id", "grades", ["enrollment_id"])


def downgrade() -> None:
    op.drop_index("ix_grades_enrollment_id", table_name="grades")
    op.drop_table("grades")