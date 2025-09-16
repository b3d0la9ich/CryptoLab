from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )
    op.create_table('lab',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('algorithm', sa.String(length=50), nullable=False),
        sa.Column('payload', sa.Text(), nullable=False),
        sa.Column('answer_hash', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )
    op.create_table('submission',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('lab_id', sa.Integer(), sa.ForeignKey('lab.id'), nullable=False),
        sa.Column('submitted_text', sa.Text(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

def downgrade():
    op.drop_table('submission')
    op.drop_table('lab')
    op.drop_table('user')
