"""initial migration.

Revision ID: a386a7a3761b
Revises: 
Create Date: 2021-06-20 16:47:04.928760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a386a7a3761b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('iduser', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('jmbg', sa.String(length=14), nullable=False),
    sa.Column('forename', sa.String(length=256), nullable=False),
    sa.Column('surname', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('role', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('iduser'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('iduser'),
    sa.UniqueConstraint('jmbg')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
