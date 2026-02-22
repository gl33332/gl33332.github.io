function initializeCard() {
  cardTimes();
  cardRefreshTimes();
}

let year, month, week, date, dates, weekStr, monthStr, asideTime, asideDay;
const now = new Date();

function cardRefreshTimes() {
  const e = document.getElementById("card-widget-schedule");
  if (e) {
    asideTime = new Date("2026/01/01 00:00:00");
    asideDay = (now - asideTime) / 86400000;
    e.querySelector("#pBar_year").value = asideDay;
    e.querySelector("#p_span_year").innerHTML = ((asideDay / 365) * 100).toFixed(1) + "%";
    e.querySelector(".schedule-r0 .aside-span2 a").innerHTML = Math.max(0, (365 - asideDay).toFixed(0));
    
    const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    e.querySelector("#pBar_month").value = now.getDate();
    e.querySelector("#pBar_month").max = daysInMonth;
    e.querySelector("#p_span_month").innerHTML = ((now.getDate() / daysInMonth) * 100).toFixed(1) + "%";
    e.querySelector(".schedule-r1 .aside-span2 a").innerHTML = Math.max(0, daysInMonth - now.getDate());

    const dayIndex = ((now.getDay() + 6) % 7) + 1;
    const weekRemaining = Math.max(0, 7 - dayIndex);
    const weekPercent = ((dayIndex / 7) * 100).toFixed(1) + "%";

    const pBarWeek = e.querySelector("#pBar_week");
    const pSpanWeek = e.querySelector("#p_span_week");
    const pWeekRemain = e.querySelector(".schedule-r2 .aside-span2 a");

    if (pBarWeek) {
      pBarWeek.max = 7;
      pBarWeek.value = dayIndex;
    }
    if (pSpanWeek) pSpanWeek.innerHTML = weekPercent;
    if (pWeekRemain) pWeekRemain.innerHTML = weekRemaining;
  }
}

function cardTimes() {
  year = now.getFullYear();
  month = now.getMonth();
  week = now.getDay();
  date = now.getDate();

  const e = document.getElementById("card-widget-calendar");
  if (e) {
    weekStr = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][week];
    const isLeap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
    const monthData = [31, isLeap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    dates = monthData[month];

    const firstDay = new Date(year, month, 1).getDay();
    const c = e.querySelector("#calendar-main");
    c.innerHTML = "";

    let n = 1;

    const rowsCount = (firstDay + dates) <= 35 ? 5 : 6;

    for (let i = 0; i < rowsCount; i++) {
      const row = document.createElement("div");
      row.className = "calendar-rh";
      for (let j = 0; j < 7; j++) {
        const cell = document.createElement("div");
        cell.className = "calendar-d0";

        const isInThisMonth = (i === 0 && j >= firstDay && n <= dates) || (i > 0 && n <= dates);
        if (isInThisMonth) {
          const isToday = n === date ? " class='now'" : "";
          cell.innerHTML = `<a${isToday}>${n}</a>`;
          n++;
        } else {
          cell.innerHTML = `<a class='empty'></a>`;
        }

        row.appendChild(cell);
      }
      c.appendChild(row);
    }

    // 农历逻辑（修复时间边界问题）
    if (typeof chineseLunar !== 'undefined') {
        const today = new Date(year, month, date); // 强制 00:00:00 避免跨日误差
        const lunarDate = chineseLunar.solarToLunar(today);
        const animalYear = chineseLunar.format(lunarDate, "A");
        const ganzhiYear = chineseLunar.format(lunarDate, "T").slice(0, -1);
        const lunarMon = chineseLunar.format(lunarDate, "M");
        const lunarDay = chineseLunar.format(lunarDate, "d");
        const lunarElem = e.querySelector("#calendar-lunar");
        if (lunarElem) lunarElem.innerHTML = `${ganzhiYear}${animalYear}年&nbsp;${lunarMon}${lunarDay}`;
    }

    const nyDate = new Date("2027/02/05 00:00:00");
    const daysToNY = Math.ceil((nyDate - now) / 86400000);
    const dayOfYear = Math.floor((now - new Date(year, 0, 1)) / 86400000) + 1;

    e.querySelector("#calendar-week").innerHTML = `第${Math.ceil((date + firstDay) / 7)}周&nbsp;${weekStr}`;
    e.querySelector("#calendar-date").innerHTML = date.toString().padStart(2, "0");
    e.querySelector("#calendar-solar").innerHTML = `${year}年${month+1}月&nbsp;第${dayOfYear}天`;
    const sd = document.getElementById("schedule-days");
    if (sd) sd.innerHTML = daysToNY;
  }
}

document.addEventListener("DOMContentLoaded", initializeCard);
document.addEventListener("pjax:complete", initializeCard);