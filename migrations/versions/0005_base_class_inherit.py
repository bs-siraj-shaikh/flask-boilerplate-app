"""Base class inherit

Revision ID: 0005
Revises: 0004
Create Date: 2024-06-27 15:39:18.847289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('uuid', sa.String(), nullable=True))
    op.add_column('student', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('student', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('student', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.add_column('student', sa.Column('email', sa.String(), nullable=False))
    op.add_column('student', sa.Column('password', sa.String(), nullable=True))
    op.add_column('student', sa.Column('auth_token', sa.String(), nullable=True))
    op.alter_column('student', 'clas',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_unique_constraint(None, 'student', ['email'])
    op.create_unique_constraint(None, 'student', ['uuid'])
    op.drop_column('student', 'sid')
    sa.PrimaryKeyConstraint('id')
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('sid', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'student', type_='unique')
    op.drop_constraint(None, 'student', type_='unique')
    op.alter_column('student', 'clas',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('student', 'auth_token')
    op.drop_column('student', 'password')
    op.drop_column('student', 'email')
    op.drop_column('student', 'id')
    op.drop_column('student', 'updated_at')
    op.drop_column('student', 'created_at')
    op.drop_column('student', 'uuid')
    # ### end Alembic commands ###