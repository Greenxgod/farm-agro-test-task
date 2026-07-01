"""initial migration

Revision ID: 8cd383700727
Revises: 
Create Date: 2026-06-29 02:47:06.927743

"""
from alembic import op
import sqlalchemy as sa


revision = '8cd383700727'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('farms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('reproduction_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('farm_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('abort', sa.Integer(), nullable=True),
    sa.Column('bulls_from_cows', sa.Integer(), nullable=True),
    sa.Column('bulls_from_heifers', sa.Integer(), nullable=True),
    sa.Column('conception_cows', sa.Integer(), nullable=True),
    sa.Column('conception_heifers', sa.Integer(), nullable=True),
    sa.Column('cows_from_cows', sa.Integer(), nullable=True),
    sa.Column('cows_from_heifers', sa.Integer(), nullable=True),
    sa.Column('dead_bulls', sa.Integer(), nullable=True),
    sa.Column('dead_heifers', sa.Integer(), nullable=True),
    sa.Column('preg_rate_cows', sa.Float(), nullable=True),
    sa.Column('preg_rate_heifers', sa.Float(), nullable=True),
    sa.Column('reproduction_cows', sa.Integer(), nullable=True),
    sa.Column('reproduction_heifers', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('abort >= 0', name='check_abort_non_negative'),
    sa.CheckConstraint('bulls_from_cows >= 0', name='check_bulls_from_cows_non_negative'),
    sa.CheckConstraint('bulls_from_heifers >= 0', name='check_bulls_from_heifers_non_negative'),
    sa.CheckConstraint('conception_cows >= 0', name='check_conception_cows_non_negative'),
    sa.CheckConstraint('conception_heifers >= 0', name='check_conception_heifers_non_negative'),
    sa.CheckConstraint('cows_from_cows >= 0', name='check_cows_from_cows_non_negative'),
    sa.CheckConstraint('cows_from_heifers >= 0', name='check_cows_from_heifers_non_negative'),
    sa.CheckConstraint('dead_bulls >= 0', name='check_dead_bulls_non_negative'),
    sa.CheckConstraint('dead_heifers >= 0', name='check_dead_heifers_non_negative'),
    sa.CheckConstraint('preg_rate_cows >= 0 AND preg_rate_cows <= 100', name='check_preg_rate_cows_range'),
    sa.CheckConstraint('preg_rate_heifers >= 0 AND preg_rate_heifers <= 100', name='check_preg_rate_heifers_range'),
    sa.CheckConstraint('reproduction_cows >= 0', name='check_reproduction_cows_non_negative'),
    sa.CheckConstraint('reproduction_heifers >= 0', name='check_reproduction_heifers_non_negative'),
    sa.ForeignKeyConstraint(['farm_id'], ['farms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('farm_id', 'date', name='unique_farm_date')
    )


def downgrade():
    op.drop_table('reproduction_records')
    op.drop_table('farms')
