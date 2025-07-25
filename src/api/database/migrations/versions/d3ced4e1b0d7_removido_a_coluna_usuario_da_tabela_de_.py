"""removido a coluna usuario da tabela de usuarios

Revision ID: d3ced4e1b0d7
Revises: 356f35356e5d
Create Date: 2025-05-21 20:39:30.122806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd3ced4e1b0d7'
down_revision: Union[str, None] = '356f35356e5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('usuario', table_name='usuarios')
    op.drop_column('usuarios', 'usuario')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuarios', sa.Column('usuario', mysql.VARCHAR(length=100), nullable=False))
    op.create_index('usuario', 'usuarios', ['usuario'], unique=True)
    # ### end Alembic commands ###
