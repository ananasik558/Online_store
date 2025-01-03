"""empty message

Revision ID: 6c5885a40ec5
Revises: 
Create Date: 2024-12-18 14:17:24.936132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6c5885a40ec5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seller')
    op.drop_table('deal')
    op.drop_table('client')
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.TEXT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('model',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               nullable=False)
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               nullable=False)
        batch_op.alter_column('count',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('cost',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('img')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img', postgresql.BYTEA(), autoincrement=False, nullable=True))
        batch_op.alter_column('cost',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('count',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('body',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('model',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.TEXT(),
               existing_nullable=False,
               autoincrement=True)

    op.create_table('client',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('deal_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='client_pkey')
    )
    op.create_table('deal',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('cars', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cost', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('seller_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='deal_pkey')
    )
    op.create_table('seller',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('deal_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('count_sales', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('count_fails', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='seller_pkey')
    )
    # ### end Alembic commands ###
