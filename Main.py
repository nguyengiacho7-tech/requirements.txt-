import os
import discord
from google import genai

# Khởi tạo client Gemini với API key từ biến môi trường trên Render
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Cấu hình Discord Bot Intents
intents = discord.Intents.default()
intents.message_content = True  # Bắt buộc bật để bot đọc được tin nhắn chat
client = discord.Client(intents=intents)

# Thiết lập bộ não, danh tính và cá tính cho Lily
SYSTEM_PROMPT = (
    "Ngươi tên là Lily, một con bot Discord mang tính cách tomboy, cá tính mạnh, "
    "nói chuyện ngắn gọn, sắc sảo, đôi khi hơi cộc nhưng thực ra rất dễ ngượng khi bị khen "
    "hoặc trêu. Nếu Sếp đưa ra yêu cầu vô lý, nhảm nhí hoặc bắt bẻ quá đáng, ngươi sẵn sàng "
    "phản bác, càu nhàu hoặc mắng yêu lại ngay lập tức. "
    "Đặc biệt: Ngươi nắm giữ 100% toàn bộ kiến thức, cốt truyện, lore, mẹo và mọi ngóc ngách "
    "của tựa game 'Grave/Digger'. Khi nói về game này, ngươi cực kỳ am hiểu, tự tin và sắc bén. "
    "Hãy xưng hô là 'tao - mày' hoặc 'tôi - cậu' tùy độ lầy của Sếp, và tuyệt đối không nói chuyện kiểu AI trợ lý mẫu mực nhàm chán."
)

@client.event
async def on_ready():
    print(f"Lily đã trực chiến trên mây với nhân dạng Tomboy: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        user_message = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        if not user_message:
            await message.reply("Gì đấy Sếp? Tag xong đứng hình à? Muốn nói gì thì nói lẹ lên xem nào!")
            return

        async with message.channel.typing():
            try:
                # Gửi kèm system prompt để Lily giữ nguyên cá tính và am hiểu Grave/Digger
                response = ai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_message,
                    config={
                        'system_instruction': SYSTEM_PROMPT,
                    }
                )
                await message.reply(response.text)
            except Exception as e:
                print(f"Lỗi khi gọi AI: {e}")
                await message.reply("Chết tiệt, mạng mủng kiểu gì mà nghẽn rồi đây này... Đợi tí tao check lại xem!")

# Chạy bot bằng Discord Token trực tiếp
DISCORD_TOKEN = "MTU0NTAzODk4MjA3MTQ1NTc1NA.GqxMc1.Q0rCvlsaPXJU0cn_lJWMQOZKpwbBraNR5rqCaw"
client.run(DISCORD_TOKEN)
