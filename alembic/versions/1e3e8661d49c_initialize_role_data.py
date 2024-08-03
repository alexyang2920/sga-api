"""initialize role data

Revision ID: 1e3e8661d49c
Revises: a8d93b70b628
Create Date: 2024-08-03 00:52:41.155023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e3e8661d49c'
down_revision: Union[str, None] = 'a8d93b70b628'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            'roles',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String)
        ),
        [
            {'id': 1, 'name': 'Admin'},
            {'id': 2, 'name': 'Users'},
            {'id': 3, 'name': 'Volunteers'},
            {'id': 4, 'name': 'Mentors'}
        ]
    )


def downgrade() -> None:
    op.execute('Delete from roles')
