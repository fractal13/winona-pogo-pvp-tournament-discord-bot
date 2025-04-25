#!/usr/bin/env python3

import interactions

async def admin_channel_check(ctx: interactions.SlashContext):
    if not ctx.channel_id in ctx.client.winona.ADMIN_CHANNEL_IDS:
        await ctx.send("This command can only be used in the admin channel.")
        return False
    else:
        return True
