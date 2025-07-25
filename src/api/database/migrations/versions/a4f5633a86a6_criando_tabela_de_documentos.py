"""criando tabela de documentos

Revision ID: a4f5633a86a6
Revises: aabf86a23a3c
Create Date: 2025-06-30 22:11:14.792948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a4f5633a86a6'
down_revision: Union[str, None] = 'aabf86a23a3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('processed_docs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('nome_arquivo', sa.String(length=500), nullable=False),
    sa.Column('nome_documento', sa.String(length=500), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('faiss_ids', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('processed_docs')
    # ### end Alembic commands ###
