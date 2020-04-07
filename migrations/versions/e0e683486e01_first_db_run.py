"""first db run

Revision ID: e0e683486e01
Revises: 
Create Date: 2020-03-29 14:49:55.680842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0e683486e01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('camera',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('camera_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qcformdb',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('editor_name', sa.String(length=64), nullable=True),
    sa.Column('producer_name', sa.String(length=64), nullable=True),
    sa.Column('program_name', sa.String(length=64), nullable=True),
    sa.Column('source_id', sa.String(length=120), nullable=True),
    sa.Column('exported_id', sa.String(length=120), nullable=True),
    sa.Column('comments', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_qcformdb_comments'), 'qcformdb', ['comments'], unique=False)
    op.create_index(op.f('ix_qcformdb_editor_name'), 'qcformdb', ['editor_name'], unique=False)
    op.create_index(op.f('ix_qcformdb_exported_id'), 'qcformdb', ['exported_id'], unique=False)
    op.create_index(op.f('ix_qcformdb_producer_name'), 'qcformdb', ['producer_name'], unique=False)
    op.create_index(op.f('ix_qcformdb_program_name'), 'qcformdb', ['program_name'], unique=False)
    op.create_index(op.f('ix_qcformdb_source_id'), 'qcformdb', ['source_id'], unique=False)
    op.create_index(op.f('ix_qcformdb_timestamp'), 'qcformdb', ['timestamp'], unique=False)
    op.create_table('sound',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sound_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cameras',
    sa.Column('camera_id', sa.Integer(), nullable=False),
    sa.Column('qcformdb_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['camera_id'], ['camera.id'], ),
    sa.ForeignKeyConstraint(['qcformdb_id'], ['qcformdb.id'], ),
    sa.PrimaryKeyConstraint('camera_id', 'qcformdb_id')
    )
    op.create_table('sounds',
    sa.Column('sound_id', sa.Integer(), nullable=False),
    sa.Column('qcformdb_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['qcformdb_id'], ['qcformdb.id'], ),
    sa.ForeignKeyConstraint(['sound_id'], ['sound.id'], ),
    sa.PrimaryKeyConstraint('sound_id', 'qcformdb_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sounds')
    op.drop_table('cameras')
    op.drop_table('sound')
    op.drop_index(op.f('ix_qcformdb_timestamp'), table_name='qcformdb')
    op.drop_index(op.f('ix_qcformdb_source_id'), table_name='qcformdb')
    op.drop_index(op.f('ix_qcformdb_program_name'), table_name='qcformdb')
    op.drop_index(op.f('ix_qcformdb_producer_name'), table_name='qcformdb')
    op.drop_index(op.f('ix_qcformdb_exported_id'), table_name='qcformdb')
    op.drop_index(op.f('ix_qcformdb_editor_name'), table_name='qcformdb')
    op.drop_index(op.f('ix_qcformdb_comments'), table_name='qcformdb')
    op.drop_table('qcformdb')
    op.drop_table('camera')
    # ### end Alembic commands ###