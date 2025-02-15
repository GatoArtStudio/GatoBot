import pytest
from service.data_base_discord import DataBaseDiscord

@pytest.fixture
def db():
    """Inicializa la base de datos en memoria para pruebas"""
    db = DataBaseDiscord(':memory:')  # Usar una base de datos en memoria para pruebas
    db.create_tables_guild_config()
    return db

def test_create_guild_config(db):
    """Prueba la creación de la configuración de un servidor"""
    assert db.create_guild_config(1) is True
    config = db.get_guild_config(1)
    
    assert isinstance(config, dict)  # Verificar que devuelve un diccionario
    assert config['guild_id'] == 1
    assert config['log_channel_id'] == 0  # Valor por defecto

def test_get_guild_config(db):
    """Prueba la recuperación de la configuración de un servidor"""
    db.create_guild_config(1, log_channel_id=123)
    config = db.get_guild_config(1)
    
    assert isinstance(config, dict)
    assert config['guild_id'] == 1
    assert config['log_channel_id'] == 123

def test_update_guild_config(db):
    """Prueba que `create_guild_config` actualiza solo los campos modificados sin sobrescribir los demás."""
    
    db.create_guild_config(1, log_channel_id=0, warning_channel_id=100)  # Crear registro inicial
    db.create_guild_config(1, log_channel_id=123)  # Modificar solo log_channel_id
    db.create_guild_config(1, sanction_channel_id=456)  # Modificar solo sanction_channel_id
    
    config = db.get_guild_config(1)
    
    assert config['log_channel_id'] == 123  # ✅ Debe reflejar el nuevo valor
    assert config['warning_channel_id'] == 100  # ✅ Debe mantenerse sin cambios
    assert config['sanction_channel_id'] == 456  # ✅ Debe reflejar el nuevo valor
