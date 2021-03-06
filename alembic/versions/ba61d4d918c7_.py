"""empty message

Revision ID: ba61d4d918c7
Revises:
Create Date: 2021-05-04 04:02:59.603178

"""
import sqlalchemy as sa
from sqlalchemy.sql import text

from alembic import op

# revision identifiers, used by Alembic.
revision = "ba61d4d918c7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    op.create_table(
        "tracking_regions",
        sa.Column(
            "id",
            sa.String(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("state_id", sa.String(), nullable=False),
        sa.Column("district_id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tracking_regions_district_id"),
        "tracking_regions",
        ["district_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_tracking_regions_state_id"),
        "tracking_regions",
        ["state_id"],
        unique=False,
    )
    op.create_table(
        "slack_user_subscriptions",
        sa.Column(
            "id",
            sa.String(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("slack_id", sa.String(), nullable=False),
        sa.Column("region_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["region_id"], ["tracking_regions.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_slack_user_subscriptions_slack_id"),
        "slack_user_subscriptions",
        ["slack_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_slack_user_subscriptions_slack_id"),
        table_name="slack_user_subscriptions",
    )
    op.drop_table("slack_user_subscriptions")
    op.drop_index(op.f("ix_tracking_regions_state_id"), table_name="tracking_regions")
    op.drop_index(
        op.f("ix_tracking_regions_district_id"), table_name="tracking_regions"
    )
    op.drop_table("tracking_regions")
    # ### end Alembic commands ###
