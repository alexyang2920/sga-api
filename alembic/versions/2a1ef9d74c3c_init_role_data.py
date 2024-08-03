"""init role data

Revision ID: 2a1ef9d74c3c
Revises: d87049569cd5
Create Date: 2024-08-03 17:32:53.009575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a1ef9d74c3c'
down_revision: Union[str, None] = 'd87049569cd5'
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
            {'id': 2, 'name': 'User'},
            {'id': 3, 'name': 'Volunteer'},
            {'id': 4, 'name': 'Mentor'}
        ]
    )


def downgrade() -> None:
    op.execute('Delete from roles')
