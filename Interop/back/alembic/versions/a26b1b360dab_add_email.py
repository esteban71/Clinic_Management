"""add email

Revision ID: a26b1b360dab
Revises: c35c1a5226a1
Create Date: 2024-11-03 10:09:28.965904

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a26b1b360dab'
down_revision: Union[str, None] = 'c35c1a5226a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('email', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patients', 'email')
    # ### end Alembic commands ###
