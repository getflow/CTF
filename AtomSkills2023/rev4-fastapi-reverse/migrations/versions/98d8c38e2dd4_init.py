"""init

Revision ID: 98d8c38e2dd4
Revises: 
Create Date: 2023-06-15 07:10:44.649725

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '98d8c38e2dd4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('project',
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('owner_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('project_id')
    )
    op.create_table('commit',
    sa.Column('commit_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('parent_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('author', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('message', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('diff', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['author'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['commit.commit_id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], ),
    sa.PrimaryKeyConstraint('commit_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commit')
    op.drop_table('project')
    op.drop_table('user')
    # ### end Alembic commands ###
