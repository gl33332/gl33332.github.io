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
    // 这里的查询路径必须精确匹配 aside.yml 里的层级
    e.querySelector(".schedule-r0 .aside-span2 a").innerHTML = Math.max(0, (365 - asideDay).toFixed(0));
    
    const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    e.querySelector("#pBar_month").value = now.getDate();
    e.querySelector("#pBar_month").max = daysInMonth;
    e.querySelector("#p_span_month").innerHTML = ((now.getDate() / daysInMonth) * 100).toFixed(1) + "%";
    e.querySelector(".schedule-r1 .aside-span2 a").innerHTML = Math.max(0, daysInMonth - now.getDate());
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

    // 计算日历起始位置
    const firstDay = new Date(year, month, 1).getDay();
    const c = e.querySelector("#calendar-main");
    c.innerHTML = "";

    let n = 1;
    // 关键修复：确保 class 名字与你的 schedule.css 布局匹配
    for (let i = 0; i < 6; i++) {
      const row = document.createElement("div");
      row.className = "calendar-rh"; // 使用 row 布局类名
      for (let j = 0; j < 7; j++) {
        const cell = document.createElement("div");
        cell.className = "calendar-d0"; // 使用 cell 布局类名
        if ((i === 0 && j >= firstDay) || (i > 0 && n <= dates)) {
          const isToday = n === date ? " class='now'" : "";
          cell.innerHTML = `<a${isToday}>${n}</a>`;
          n++;
        }
        row.appendChild(cell);
      }
      c.appendChild(row);
      if (n > dates) break;
    }

    // 农历逻辑
    if (typeof chineseLunar !== 'undefined') {
        const lunarDate = chineseLunar.solarToLunar(now);
        const animalYear = chineseLunar.format(lunarDate, "A");
        const ganzhiYear = chineseLunar.format(lunarDate, "T").slice(0, -1);
        const lunarMon = chineseLunar.format(lunarDate, "M");
        const lunarDay = chineseLunar.format(lunarDate, "d");
        const lunarElem = e.querySelector("#calendar-lunar");
        if(lunarElem) lunarElem.innerHTML = `${ganzhiYear}${animalYear}年&nbsp;${lunarMon}${lunarDay}`;
    }

    const nyDate = new Date("2026/02/17 00:00:00");
    const daysToNY = Math.ceil((nyDate - now) / 86400000);
    const dayOfYear = Math.floor((now - new Date(year, 0, 1)) / 86400000) + 1;

    e.querySelector("#calendar-week").innerHTML = `第${Math.ceil((date + firstDay) / 7)}周&nbsp;${weekStr}`;
    e.querySelector("#calendar-date").innerHTML = date.toString().padStart(2, "0");
    e.querySelector("#calendar-solar").innerHTML = `${year}年${month+1}月&nbsp;第${dayOfYear}天`;
    const sd = document.getElementById("schedule-days");
    if(sd) sd.innerHTML = daysToNY;
  }
}

document.addEventListener("DOMContentLoaded", initializeCard);
document.addEventListener("pjax:complete", initializeCard);