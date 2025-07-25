"""criando as tabelas para o agente de ia

Revision ID: 356f35356e5d
Revises: 
Create Date: 2025-05-21 20:09:31.393455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '356f35356e5d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usuario', sa.String(length=100), nullable=False),
    sa.Column('nome_completo', sa.String(length=255), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('celular1', sa.String(length=15), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('celular2', sa.String(length=15), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('permissoes', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('acess_token', sa.String(length=255), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('refresh_token_exp', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('usuario')
    )
    op.create_table('agent_memory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('descricao_memoria', sa.Text(), nullable=False),
    sa.Column('faiss_id', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('historico_chat',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('thread_id', sa.String(length=255), nullable=False),
    sa.Column('texto_chat', sa.Text(), nullable=False),
    sa.Column('origem', sa.String(length=50), nullable=False, comment='Usuário ou IA'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('historico_chat')
    op.drop_table('agent_memory')
    op.drop_table('usuarios')
    # ### end Alembic commands ###
