//@version=5
strategy("SMC_5of6_Volume_Arrows_V4", overlay=true, initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=1)

// =================================================================
// 1. НАСТРОЙКИ ВХОДНЫХ ПАРАМЕТРОВ (INPUTS)
// =================================================================
// Ваши исходные настройки
i_ma_period = input.int(50, title="5M SMA Length")
i_smc_lookback = input.int(5, title="SMC Lookback Period") 

// Настройки для ФИЛЬТРОВ
ema_1h_length = input.int(50, title="1H EMA Length (Trend Filter)")
stoch_k_length = input.int(14, title="Stoch K Length")
stoch_smooth = input.int(3, title="Stoch Smooth")
volume_avg_period = input.int(20, title="Volume Average Period")
volume_multiplier = input.float(1.5, title="Volume Spike Multiplier (e.g., 1.5x)")

// Webhook-сообщения (Используются для Telegram/Webhook)
long_message = '{ "strategy": "SMC_5OF6_VOL", "symbol": "{{ticker}}", "action": "BUY", "price": "{{close}}", "timeframe": "5m" }'
short_message = '{ "strategy": "SMC_5OF6_VOL", "symbol": "{{ticker}}", "action": "SELL", "price": "{{close}}", "timeframe": "5m" }'


// =================================================================
// 2. РАСЧЕТ ИНДИКАТОРОВ
// =================================================================

// F6 (Исходная SMC Proxy)
ma_50 = ta.sma(close, i_ma_period)

// F1: ГЛОБАЛЬНЫЙ ТРЕНД (1H EMA)
ema_1h = request.security(syminfo.tickerid, "60", ta.ema(close, ema_1h_length))

// F3, F5: ОСЦИЛЛЯТОРЫ (Stochastic, MACD)
stoch_k = ta.stoch(close, high, low, stoch_k_length)
stoch_d = ta.sma(stoch_k, stoch_smooth)
[macd_line, signal_line, _] = ta.macd(close, 12, 26, 9)

// F4: Подтверждение Объемом
avg_volume = ta.sma(volume, volume_avg_period)


// =================================================================
// 3. ОПРЕДЕЛЕНИЕ УСЛОВИЙ (6 ФАКТОРОВ)
// =================================================================

// LONG Условия
proxy_condition_long = (close > ma_50 and close > ta.highest(high[1], i_smc_lookback))
trend_ok_long = close > ema_1h 
zone_ok_long = low < low[1] and close > open 
stoch_ok_long = ta.cross(stoch_k, stoch_d) and stoch_k < 40 
volume_ok_long = volume > avg_volume * volume_multiplier 
macd_ok_long = macd_line > signal_line 


// SHORT Условия
proxy_condition_short = (close < ma_50 and close < ta.lowest(low[1], i_smc_lookback))
trend_ok_short = close < ema_1h 
zone_ok_short = high > high[1] and close < open 
stoch_ok_short = ta.cross(stoch_d, stoch_k) and stoch_k > 60 
volume_ok_short = volume > avg_volume * volume_multiplier 
macd_ok_short = macd_line < signal_line 


// =================================================================
// 4. ЛОГИКА СЧЕТЧИКА (5 ИЗ 6 ФАКТОРОВ)
// =================================================================

long_factors_count = 0
short_factors_count = 0

// Начисление баллов LONG
if proxy_condition_long
    long_factors_count += 1
if trend_ok_long
    long_factors_count += 1
if zone_ok_long
    long_factors_count += 1
if stoch_ok_long
    long_factors_count += 1
if volume_ok_long
    long_factors_count += 1
if macd_ok_long
    long_factors_count += 1

// Начисление баллов SHORT
if proxy_condition_short
    short_factors_count += 1
if trend_ok_short
    short_factors_count += 1
if zone_ok_short
    short_factors_count += 1
if stoch_ok_short
    short_factors_count += 1
if volume_ok_short
    short_factors_count += 1
if macd_ok_short
    short_factors_count += 1

// Окончательное условие входа: 5 или 6 факторов
long_entry_condition = long_factors_count >= 5
short_entry_condition = short_factors_count >= 5


// =================================================================
// 5. ОТПРАВКА СИГНАЛОВ (АЛЕРТЫ)
// =================================================================

if long_entry_condition
    alert(long_message, alert.freq_once_per_bar)

if short_entry_condition
    alert(short_message, alert.freq_once_per_bar)


// =================================================================
// 6. ВИЗУАЛИЗАЦИЯ (СТРЕЛКИ И КРУЖКИ)
// =================================================================

// 6.1. Визуализация скользящих средних
plot(ma_50, title="5M SMA 50", color=color.new(color.purple, 0))
plot(ema_1h, title="1H EMA 50 (Trend Filter)", color=color.new(color.blue, 0), linewidth=2)

// 6.2. Стрелки (Основной сигнал)
// Зеленая стрелка ВНИЗ (для LONG)
plotshape(long_entry_condition, title="BUY Arrow", 
          style=shape.triangleup, 
          location=location.belowbar, 
          color=color.new(color.lime, 0), 
          size=size.normal)

// Красная стрелка ВВЕРХ (для SHORT)
plotshape(short_entry_condition, title="SELL Arrow", 
          style=shape.triangledown, 
          location=location.abovebar, 
          color=color.new(color.red, 0), 
          size=size.normal)

// 6.3. Кружки (Подтверждение)
// Кружок для подтверждения входа (помещается на саму стрелку)
plotchar(long_entry_condition, title="BUY Confirmation Circle", 
         char='●', // Используем символ кружка
         location=location.belowbar, 
         color=color.new(color.white, 0), 
         size=size.small, 
         offset=0)

plotchar(short_entry_condition, title="SELL Confirmation Circle", 
         char='●', 
         location=location.abovebar, 
         color=color.new(color.white, 0), 
         size=size.small, 
         offset=0)

// 6.4. Визуализация счетчика (показывает количество совпавших факторов)
plot(long_factors_count > 0 ? long_factors_count : na, 
     title="Long Factors Count", 
     color=color.new(color.green, 0), 
     style=plot.style_columns, 
     histbase=0)
plot(short_factors_count > 0 ? short_factors_count : na, 
     title="Short Factors Count", 
     color=color.new(color.red, 0), 
     style=plot.style_columns, 
     histbase=0)
