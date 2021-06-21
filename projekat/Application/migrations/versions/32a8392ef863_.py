"""empty message

Revision ID: 32a8392ef863
Revises: d81550d3dc04
Create Date: 2021-06-21 13:38:37.292684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32a8392ef863'
down_revision = 'd81550d3dc04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('idvote', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('guid', sa.String(length=256), nullable=False),
    sa.Column('pollnumber', sa.Integer(), nullable=False),
    sa.Column('election', sa.Integer(), nullable=True),
    sa.Column('valid', sa.Boolean(), nullable=False),
    sa.Column('reason', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['election'], ['elections.idelection'], ),
    sa.PrimaryKeyConstraint('idvote'),
    sa.UniqueConstraint('idvote')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
