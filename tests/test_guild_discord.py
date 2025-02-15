import pytest
from base.guild_discord import GuildDiscord
from service.data_base_discord import DataBaseDiscord

@pytest.fixture
def guild():
    db = DataBaseDiscord(':memory:')  # Usar una base de datos en memoria para pruebas
    db.create_tables_guild_config()
    return GuildDiscord(1)

def test_set_log_channel(guild):
    guild.set_log_channel(123)
    assert guild.get_log_channel() == 123

def test_get_log_channel(guild):
    guild.set_log_channel(123)
    assert guild.get_log_channel() == 123

def test_get_guild_config(guild):
    guild.set_log_channel(127)
    result = guild._get_guild_config()
    assert result['log_channel_id'] == 127

def test_setters_and_getters_guild_discord(guild):
    guild.set_log_channel(538)
    guild.set_warning_channel(924)
    guild.set_announcement_channel(392)
    guild.set_sanction_channel(3380439051)

    assert guild.get_log_channel() == 538
    assert guild.get_warning_channel() == 924
    assert guild.get_announcement_channel() == 392
    assert guild.get_sanction_channel() == 3380439051
