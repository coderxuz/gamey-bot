"""userGame change users.id to users.tg_id

Revision ID: 6d837df66793
Revises: fa9ee49d6a05
Create Date: 2025-02-17 17:37:43.951310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d837df66793'
down_revision: Union[str, None] = 'fa9ee49d6a05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_game_user_tg_id_fkey', 'user_game', type_='foreignkey')
    op.create_foreign_key(None, 'user_game', 'users', ['user_tg_id'], ['tg_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_game', type_='foreignkey')
    op.create_foreign_key('user_game_user_tg_id_fkey', 'user_game', 'users', ['user_tg_id'], ['id'])
    # ### end Alembic commands ###
