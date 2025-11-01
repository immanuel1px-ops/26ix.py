# 🔥 CORREÇÃO DO AUDIOOP - ADICIONAR NO INÍCIO DO ARQUIVO
import os
os.environ['DISCORD_INSTALL_VOICE'] = '0'  # Desativa funcionalidades de voz

# Forçar reinstalação do discord.py sem suporte a voz se necessário
import subprocess
import sys
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py==2.3.2"])
except:
    pass

import discord
from discord.ext import commands
import asyncio
import datetime
import json
import os
from typing import Dict, List
from flask import Flask
from threading import Thread

# CONFIGURAÇÃO
TOKEN = os.environ.get('DISCORD_TOKEN')
PREFIX = "s!"

# CONFIGURAÇÕES
TICKET_CATEGORY_NAME = "tickets"
SUPPORT_ROLE_NAME = "Support Team"
LOG_CHANNEL_NAME = "logs"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
intents.reactions = True
intents.moderation = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# SISTEMA DE ARMAZENAMENTO
class DataSystem:
    def __init__(self):
        self.tickets_file = "tickets.json"
        self.autoroles_file = "autoroles.json"
        self.logs_file = "logs.json"
        self.embeds_file = "embeds.json"
        self.welcome_roles_file = "welcome_roles.json"
        self.load_data()

    def load_data(self):
        """Carrega dados dos arquivos"""
        try:
            # Carregar tickets
            if os.path.exists(self.tickets_file):
                with open(self.tickets_file, 'r', encoding='utf-8') as f:
                    self.tickets_data = json.load(f)
            else:
                self.tickets_data = {}

            # Carregar autoroles
            if os.path.exists(self.autoroles_file):
                with open(self.autoroles_file, 'r', encoding='utf-8') as f:
                    self.autoroles_data = json.load(f)
            else:
                self.autoroles_data = {}

            # Carregar logs
            if os.path.exists(self.logs_file):
                with open(self.logs_file, 'r', encoding='utf-8') as f:
                    self.logs_data = json.load(f)
            else:
                self.logs_data = {}

            # Carregar embeds
            if os.path.exists(self.embeds_file):
                with open(self.embeds_file, 'r', encoding='utf-8') as f:
                    self.embeds_data = json.load(f)
            else:
                self.embeds_data = {}

            # Carregar welcome roles
            if os.path.exists(self.welcome_roles_file):
                with open(self.welcome_roles_file, 'r', encoding='utf-8') as f:
                    self.welcome_roles_data = json.load(f)
            else:
                self.welcome_roles_data = {}

        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.tickets_data = {}
            self.autoroles_data = {}
            self.logs_data = {}
            self.embeds_data = {}
            self.welcome_roles_data = {}

    def save_tickets(self):
        """Salva dados dos tickets"""
        try:
            with open(self.tickets_file, 'w', encoding='utf-8') as f:
                json.dump(self.tickets_data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar tickets: {e}")

    def save_autoroles(self):
        """Salva dados dos autoroles"""
        try:
            with open(self.autoroles_file, 'w', encoding='utf-8') as f:
                json.dump(self.autoroles_data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar autoroles: {e}")

    def save_logs(self):
        """Salva dados dos logs"""
        try:
            with open(self.logs_file, 'w', encoding='utf-8') as f:
                json.dump(self.logs_data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar logs: {e}")

    def save_embeds(self):
        """Salva dados dos embeds"""
        try:
            with open(self.embeds_file, 'w', encoding='utf-8') as f:
                json.dump(self.embeds_data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar embeds: {e}")

    def save_welcome_roles(self):
        """Salva dados dos welcome roles"""
        try:
            with open(self.welcome_roles_file, 'w', encoding='utf-8') as f:
                json.dump(self.welcome_roles_data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar welcome roles: {e}")

data_system = DataSystem()

# SISTEMA DE LOGS CORRIGIDO
class LogSystem:
    @staticmethod
    async def get_log_channel(guild):
        """Encontra ou cria canal de logs"""
        log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
        if not log_channel:
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }

                log_channel = await guild.create_text_channel(
                    name=LOG_CHANNEL_NAME,
                    overwrites=overwrites,
                    topic="Canal de logs do sistema"
                )
            except Exception as e:
                print(f"Erro ao criar canal de logs: {e}")
                return None
        return log_channel

    @staticmethod
    async def log_action(guild, action_type, **details):
        """Sistema de logs simplificado"""
        try:
            log_channel = await LogSystem.get_log_channel(guild)
            if not log_channel:
                return

            # Cores para diferentes tipos de ações
            colors = {
                'ban': 0xff0000,
                'kick': 0xffa500,
                'mute': 0x808080,
                'unmute': 0x00ff00,
                'clear': 0x00ff00,
                'ticket_create': 0x00ff00,
                'ticket_close': 0xff0000,
                'autorole_add': 0x9b59b6,
                'autorole_remove': 0xe74c3c,
                'embed_create': 0x3498db,
                'embed_send': 0x2ecc71,
                'message_delete': 0xe74c3c,
                'message_edit': 0xf39c12,
                'message_bulk_delete': 0xc0392b,
                'command_used': 0x9b59b6,
                'user_join': 0x2ecc71,
                'user_leave': 0xe74c3c,
                'role_add': 0x3498db,
                'role_remove': 0xe74c3c,
                'welcome_role_add': 0x1abc9c
            }

            embed = discord.Embed(
                title=f"Log - {action_type.replace('_', ' ').title()}",
                color=colors.get(action_type, 0x0000ff),
                timestamp=datetime.datetime.utcnow()
            )

            # Adicionar detalhes
            for key, value in details.items():
                if value and str(value).strip():
                    embed.add_field(
                        name=key.replace('_', ' ').title(),
                        value=str(value)[:1024],
                        inline=len(str(value)) < 50
                    )

            await log_channel.send(embed=embed)

            # Salvar no arquivo
            log_id = f"{guild.id}-{int(datetime.datetime.now().timestamp())}"
            data_system.logs_data[log_id] = {
                'action': action_type,
                'guild_id': guild.id,
                'timestamp': datetime.datetime.now().isoformat(),
                **details
            }
            data_system.save_logs()

        except Exception as e:
            print(f"Erro no sistema de logs: {e}")

    @staticmethod
    async def log_message_delete(message):
        """Log quando uma mensagem é deletada"""
        if not message.guild or message.author.bot:
            return

        # Limitar conteúdo muito longo
        content = message.content
        if len(content) > 500:
            content = content[:500] + "..."

        await LogSystem.log_action(
            message.guild,
            'message_delete',
            author=f"{message.author} ({message.author.id})",
            channel=message.channel.name,
            content=content,
            message_id=message.id,
            attachments_count=len(message.attachments)
        )

    @staticmethod
    async def log_message_edit(before, after):
        """Log quando uma mensagem é editada"""
        if not before.guild or before.author.bot or before.content == after.content:
            return

        # Limitar conteúdo muito longo
        before_content = before.content
        after_content = after.content
        if len(before_content) > 300:
            before_content = before_content[:300] + "..."
        if len(after_content) > 300:
            after_content = after_content[:300] + "..."

        await LogSystem.log_action(
            before.guild,
            'message_edit',
            author=f"{before.author} ({before.author.id})",
            channel=before.channel.name,
            before_content=before_content,
            after_content=after_content,
            message_id=before.id
        )

    @staticmethod
    async def log_bulk_delete(messages):
        """Log quando várias mensagens são deletadas de uma vez"""
        if not messages or not messages[0].guild:
            return

        guild = messages[0].guild
        users = {}
        total_messages = len(messages)

        for msg in messages:
            if not msg.author.bot:
                users[msg.author.id] = users.get(msg.author.id, 0) + 1

        user_summary = "\n".join([f"<@{uid}>: {count} mensagens" for uid, count in users.items()])

        await LogSystem.log_action(
            guild,
            'message_bulk_delete',
            channel=messages[0].channel.name,
            total_messages=total_messages,
            users_affected=len(users),
            user_summary=user_summary[:500] + "..." if len(user_summary) > 500 else user_summary
        )

    @staticmethod
    async def log_command(ctx):
        """Log quando um comando é usado"""
        await LogSystem.log_action(
            ctx.guild,
            'command_used',
            user=f"{ctx.author} ({ctx.author.id})",
            command=ctx.command.name,
            channel=ctx.channel.name,
            content=ctx.message.content[:200] + "..." if len(ctx.message.content) > 200 else ctx.message.content
        )

    @staticmethod
    async def log_user_join(member):
        """Log quando um usuário entra no servidor"""
        await LogSystem.log_action(
            member.guild,
            'user_join',
            user=f"{member} ({member.id})",
            account_created=member.created_at.strftime("%d/%m/%Y %H:%M"),
            member_count=member.guild.member_count
        )

    @staticmethod
    async def log_user_leave(member):
        """Log quando um usuário sai do servidor"""
        await LogSystem.log_action(
            member.guild,
            'user_leave',
            user=f"{member} ({member.id})",
            member_count=member.guild.member_count
        )

    @staticmethod
    async def log_role_change(member, role, action):
        """Log quando um cargo é adicionado/removido"""
        await LogSystem.log_action(
            member.guild,
            f'role_{action}',
            user=f"{member} ({member.id})",
            role=role.name,
            role_id=role.id
        )

    @staticmethod
    async def log_welcome_role(member, role):
        """Log quando um cargo de boas-vindas é adicionado"""
        await LogSystem.log_action(
            member.guild,
            'welcome_role_add',
            user=f"{member} ({member.id})",
            role=role.name,
            role_id=role.id
        )

log_system = LogSystem()

# SISTEMA DE CARGO AUTOMÁTICO PARA NOVOS MEMBROS
class WelcomeRoleSystem:
    @staticmethod
    async def set_welcome_role(guild_id, role_id):
        """Define o cargo automático para novos membros"""
        guild_key = str(guild_id)
        data_system.welcome_roles_data[guild_key] = role_id
        data_system.save_welcome_roles()

    @staticmethod
    async def get_welcome_role(guild_id):
        """Obtém o cargo automático configurado"""
        guild_key = str(guild_id)
        return data_system.welcome_roles_data.get(guild_key)

    @staticmethod
    async def remove_welcome_role(guild_id):
        """Remove a configuração de cargo automático"""
        guild_key = str(guild_id)
        if guild_key in data_system.welcome_roles_data:
            del data_system.welcome_roles_data[guild_key]
            data_system.save_welcome_roles()
            return True
        return False

    @staticmethod
    async def add_welcome_role(member):
        """Adiciona o cargo automático ao novo membro"""
        try:
            role_id = await WelcomeRoleSystem.get_welcome_role(member.guild.id)
            if not role_id:
                return False

            role = member.guild.get_role(int(role_id))
            if not role:
                return False

            await member.add_roles(role)
            await log_system.log_welcome_role(member, role)
            return True
        except Exception as e:
            print(f"Erro ao adicionar cargo de boas-vindas: {e}")
            return False

welcome_role_system = WelcomeRoleSystem()

# SISTEMA DE EMBEDS (simplificado para evitar erros)
class EmbedSystem:
    @staticmethod
    async def create_embed_interactive(ctx):
        """Cria embed de forma interativa"""
        try:
            embed_data = {
                'title': '',
                'description': '',
                'color': 0x3498db,
                'fields': [],
                'footer': '',
                'thumbnail': '',
                'image': ''
            }

            # Perguntar título
            await ctx.send("📝 **Digite o título do embed (ou 'pular' para pular):**")
            try:
                title_msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                if title_msg.content.lower() != 'pular':
                    embed_data['title'] = title_msg.content
            except asyncio.TimeoutError:
                await ctx.send("⏰ Tempo esgotado. Usando valores padrão.")

            # Perguntar descrição
            await ctx.send("📝 **Digite a descrição do embed (ou 'pular' para pular):**")
            try:
                desc_msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                if desc_msg.content.lower() != 'pular':
                    embed_data['description'] = desc_msg.content
            except asyncio.TimeoutError:
                pass

            return embed_data

        except Exception as e:
            await ctx.send(f"❌ Erro ao criar embed: {e}")
            return None

    @staticmethod
    def build_embed(embed_data):
        """Constrói o embed a partir dos dados"""
        embed = discord.Embed(
            title=embed_data.get('title', ''),
            description=embed_data.get('description', ''),
            color=embed_data.get('color', 0x3498db)
        )

        # Adicionar campos se existirem
        for field in embed_data.get('fields', []):
            embed.add_field(
                name=field.get('name', 'Campo'),
                value=field.get('value', 'Valor'),
                inline=field.get('inline', False)
            )

        # Adicionar footer se existir
        if embed_data.get('footer'):
            embed.set_footer(text=embed_data['footer'])

        return embed

    @staticmethod
    async def save_embed(guild_id, name, embed_data):
        """Salva embed no arquivo"""
        guild_key = str(guild_id)
        if guild_key not in data_system.embeds_data:
            data_system.embeds_data[guild_key] = {}
        data_system.embeds_data[guild_key][name] = embed_data
        data_system.save_embeds()

    @staticmethod
    async def load_embed(guild_id, name):
        """Carrega embed do arquivo"""
        guild_key = str(guild_id)
        if guild_key in data_system.embeds_data:
            return data_system.embeds_data[guild_key].get(name)
        return None

    @staticmethod
    async def list_embeds(guild_id):
        """Lista todos os embeds salvos"""
        guild_key = str(guild_id)
        if guild_key in data_system.embeds_data:
            return list(data_system.embeds_data[guild_key].keys())
        return []

embed_system = EmbedSystem()

# EVENTOS DO BOT
@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} está online!')
    print(f'🔧 Prefixo: {PREFIX}')
    print(f'🚀 Sistemas carregados: Tickets, AutoRoles, Logs, Embeds, WelcomeRoles')

    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{PREFIX}ajuda | Sistema Completo"
    )
    await bot.change_presence(activity=activity)

@bot.event
async def on_message_delete(message):
    """Log quando uma mensagem é deletada"""
    await log_system.log_message_delete(message)

@bot.event
async def on_message_edit(before, after):
    """Log quando uma mensagem é editada"""
    await log_system.log_message_edit(before, after)

@bot.event
async def on_member_join(member):
    """Quando um usuário entra no servidor"""
    await log_system.log_user_join(member)
    await welcome_role_system.add_welcome_role(member)

@bot.event
async def on_member_remove(member):
    """Log quando um usuário sai do servidor"""
    await log_system.log_user_leave(member)

@bot.event
async def on_command(ctx):
    """Log quando um comando é usado"""
    await log_system.log_command(ctx)

# COMANDOS DO SISTEMA DE CARGO AUTOMÁTICO
@bot.command()
@commands.has_permissions(manage_roles=True)
async def set_welcome_role(ctx, role: discord.Role):
    """Define um cargo para ser dado automaticamente a novos membros"""
    try:
        await welcome_role_system.set_welcome_role(ctx.guild.id, role.id)

        embed = discord.Embed(
            title="✅ Cargo de Boas-Vindas Configurado",
            description=f"Novos membros receberão automaticamente o cargo {role.mention}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)

        await log_system.log_action(
            ctx.guild,
            'welcome_role_set',
            user=f"{ctx.author} ({ctx.author.id})",
            role=role.name,
            role_id=role.id
        )

    except Exception as e:
        await ctx.send(f"❌ Erro ao configurar cargo de boas-vindas: {e}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def remove_welcome_role(ctx):
    """Remove o cargo automático de boas-vindas"""
    try:
        success = await welcome_role_system.remove_welcome_role(ctx.guild.id)

        if success:
            embed = discord.Embed(
                title="✅ Cargo de Boas-Vindas Removido",
                description="Novos membros não receberão mais cargo automaticamente",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("ℹ️ Nenhum cargo de boas-vindas estava configurado.")

    except Exception as e:
        await ctx.send(f"❌ Erro ao remover cargo de boas-vindas: {e}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def show_welcome_role(ctx):
    """Mostra o cargo automático configurado"""
    try:
        role_id = await welcome_role_system.get_welcome_role(ctx.guild.id)

        if role_id:
            role = ctx.guild.get_role(int(role_id))
            if role:
                embed = discord.Embed(
                    title="🔧 Cargo de Boas-Vindas Atual",
                    description=f"Novos membros recebem: {role.mention}",
                    color=0x3498db
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Cargo configurado não encontrado. Use `set_welcome_role` para configurar um novo.")
        else:
            await ctx.send("ℹ️ Nenhum cargo de boas-vindas configurado. Use `set_welcome_role` para configurar.")

    except Exception as e:
        await ctx.send(f"❌ Erro ao verificar cargo de boas-vindas: {e}")

# COMANDOS DE EMBEDS
@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed_create(ctx, nome_salvo: str = None):
    """Cria um embed personalizado de forma interativa"""
    try:
        embed_data = await embed_system.create_embed_interactive(ctx)
        if not embed_data:
            return

        # Construir e mostrar preview
        embed = embed_system.build_embed(embed_data)
        await ctx.send("**👀 Preview do Embed:**", embed=embed)

        # Salvar se um nome foi fornecido
        if nome_salvo:
            await embed_system.save_embed(ctx.guild.id, nome_salvo, embed_data)
            await ctx.send(f"✅ Embed salvo com sucesso como: `{nome_salvo}`")

            await log_system.log_action(
                ctx.guild,
                'embed_create',
                user=f"{ctx.author} ({ctx.author.id})",
                embed_name=nome_salvo,
                title=embed_data.get('title', 'Sem titulo')
            )

    except Exception as e:
        await ctx.send(f"❌ Erro ao criar embed: {e}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed_send(ctx, nome_embed: str, canal: discord.TextChannel = None):
    """Envia um embed salvo"""
    try:
        embed_data = await embed_system.load_embed(ctx.guild.id, nome_embed)
        if not embed_data:
            await ctx.send(f"❌ Embed `{nome_embed}` não encontrado.")
            return

        embed = embed_system.build_embed(embed_data)
        target_channel = canal or ctx.channel

        await target_channel.send(embed=embed)
        await ctx.send(f"✅ Embed `{nome_embed}` enviado para {target_channel.mention}", delete_after=5)

        await log_system.log_action(
            ctx.guild,
            'embed_send',
            user=f"{ctx.author} ({ctx.author.id})",
            embed_name=nome_embed,
            channel=target_channel.name,
            title=embed_data.get('title', 'Sem titulo')
        )

    except Exception as e:
        await ctx.send(f"❌ Erro ao enviar embed: {e}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed_list(ctx):
    """Lista todos os embeds salvos"""
    try:
        embeds = await embed_system.list_embeds(ctx.guild.id)
        if not embeds:
            await ctx.send("ℹ️ Nenhum embed salvo neste servidor.")
            return

        embed = discord.Embed(
            title="📋 Embeds Salvos",
            color=0x3498db
        )

        for i, embed_name in enumerate(embeds, 1):
            embed.add_field(
                name=f"Embed {i}",
                value=f"`{embed_name}`",
                inline=True
            )

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Erro ao listar embeds: {e}")

# COMANDOS DE MODERAÇÃO
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Não especificado"):
    """Bane um usuário"""
    try:
        await member.ban(reason=reason)

        await log_system.log_action(
            ctx.guild,
            'ban',
            moderator=f"{ctx.author} ({ctx.author.id})",
            user=f"{member} ({member.id})",
            reason=reason
        )

        embed = discord.Embed(
            title="🔨 Usuário Banido",
            color=0xff0000
        )
        embed.add_field(name="👤 Usuário", value=member.mention, inline=True)
        embed.add_field(name="🛡️ Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Motivo", value=reason, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Erro ao banir: {e}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    """Limpa mensagens"""
    try:
        if amount > 100:
            await ctx.send("❌ Máximo de 100 mensagens.")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)

        await log_system.log_action(
            ctx.guild,
            'clear',
            moderator=f"{ctx.author} ({ctx.author.id})",
            channel=ctx.channel.name,
            messages_deleted=str(len(deleted) - 1)
        )

        msg = await ctx.send(f"✅ {len(deleted) - 1} mensagens deletadas!")
        await asyncio.sleep(3)
        await msg.delete()

    except Exception as e:
        await ctx.send(f"❌ Erro ao limpar: {e}")

# COMANDO AJUDA
@bot.command()
async def ajuda(ctx):
    """Mostra todos os comandos"""
    embed = discord.Embed(
        title="🤖 Sistema Completo de Moderação",
        description=f"**Prefixo:** `{PREFIX}`",
        color=0x00ff00
    )

    embed.add_field(
        name="🎯 Sistema de Boas-Vindas",
        value=f"""
        `{PREFIX}set_welcome_role @cargo` - Define cargo automático
        `{PREFIX}remove_welcome_role` - Remove cargo automático
        `{PREFIX}show_welcome_role` - Mostra cargo configurado
        """,
        inline=False
    )

    embed.add_field(
        name="📝 Sistema de Embeds",
        value=f"""
        `{PREFIX}embed_create [nome]` - Cria embed interativo
        `{PREFIX}embed_send nome [canal]` - Envia embed salvo
        `{PREFIX}embed_list` - Lista embeds salvos
        """,
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderação",
        value=f"""
        `{PREFIX}ban @user [motivo]` - Banir usuário
        `{PREFIX}clear [quantidade]` - Limpar mensagens
        """,
        inline=False
    )

    await ctx.send(embed=embed)

# CONFIGURAÇÃO FLASK PARA UPTIMEROBOT
app = Flask('')

@app.route('/')
def home():
    return f"""
    <h1>🚀 Bot Discord Online!</h1>
    <p>Hora: {datetime.datetime.now()}</p>
    <p>Webview funcionando!</p>
    """

@app.route('/ping')
def ping():
    return "pong"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    server = Thread(target=run_flask)
    server.start()

# INICIAR TUDO
if __name__ == "__main__":
    print("🚀 Iniciando bot...")
    print("🔧 Configurações carregadas:")
    print(f"   - Prefixo: {PREFIX}")
    print(f"   - Token: {'✅ Configurado' if TOKEN else '❌ Não encontrado'}")
    
    keep_alive()
    print("🌐 Servidor web iniciado na porta 8080")
    
    try:
        if TOKEN:
            bot.run(TOKEN)
        else:
            print("❌ ERRO: Token do Discord não encontrado!")
            print("💡 Configure a variável de ambiente DISCORD_TOKEN")
    except Exception as e:
        print(f"❌ Erro ao iniciar bot: {e}")
