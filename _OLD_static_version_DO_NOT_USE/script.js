document.addEventListener('DOMContentLoaded', () => {
    // ---- Static Tasks for Frontend ----
    let initialTasks = [
        { id: 1, title: 'Revise Mechanics', time: '10:00 AM', subject: 'physics', subjectName: 'Physics', completed: false },
        { id: 2, title: 'Solve 50 Calculus MCQs', time: '02:00 PM', subject: 'maths', subjectName: 'Mathematics', completed: false },
        { id: 3, title: 'Organic Chemistry Notes', time: '04:30 PM', subject: 'chemistry', subjectName: 'Chemistry', completed: true }
    ];

    const taskList = document.getElementById('taskList');

    function renderTasks() {
        taskList.innerHTML = '';
        initialTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.completed ? 'completed' : ''}`;
            li.innerHTML = `
                <div class="task-left">
                    <div class="checkbox" data-id="${task.id}"></div>
                    <div class="task-info">
                        <h4>${task.title}</h4>
                        <p><i class="fa-regular fa-clock"></i> ${task.time}</p>
                    </div>
                </div>
                <div class="task-tag tag-${task.subject}">${task.subjectName}</div>
            `;
            taskList.appendChild(li);
        });

        // Add event listeners to checkboxes
        document.querySelectorAll('.checkbox').forEach(cb => {
            cb.addEventListener('click', (e) => {
                const id = parseInt(e.target.getAttribute('data-id'));
                const task = initialTasks.find(t => t.id === id);
                if (task) {
                    task.completed = !task.completed;
                    renderTasks();
                    updateProgressCircle();
                }
            });
        });
    }

    renderTasks();

    // ---- Timer functionality ----
    let defaultMinutes = 45;
    let defaultSeconds = 0;
    let minutesContent = defaultMinutes;
    let secondsContent = defaultSeconds;
    let timerInterval = null;
    let isRunning = false;

    const minEl = document.getElementById('minutes');
    const secEl = document.getElementById('seconds');
    const startBtn = document.getElementById('startTimer');
    const resetBtn = document.getElementById('resetTimer');

    function updateDisplay() {
        minEl.textContent = minutesContent.toString().padStart(2, '0');
        secEl.textContent = secondsContent.toString().padStart(2, '0');
    }

    startBtn.addEventListener('click', () => {
        if (isRunning) {
            clearInterval(timerInterval);
            startBtn.innerHTML = '<i class="fa-solid fa-play"></i> Start';
        } else {
            startBtn.innerHTML = '<i class="fa-solid fa-pause"></i> Pause';
            timerInterval = setInterval(() => {
                if (secondsContent === 0) {
                    if (minutesContent === 0) {
                        clearInterval(timerInterval);
                        isRunning = false;
                        startBtn.innerHTML = '<i class="fa-solid fa-play"></i> Start';
                        alert('Study session complete! Great job.');
                        return;
                    }
                    minutesContent--;
                    secondsContent = 59;
                } else {
                    secondsContent--;
                }
                updateDisplay();
            }, 1000);
        }
        isRunning = !isRunning;
    });

    resetBtn.addEventListener('click', () => {
        clearInterval(timerInterval);
        isRunning = false;
        startBtn.innerHTML = '<i class="fa-solid fa-play"></i> Start';
        minutesContent = defaultMinutes;
        secondsContent = defaultSeconds;
        updateDisplay();
    });

    // ---- Modal logic ----
    const modal = document.getElementById('taskModal');
    const addBtn = document.getElementById('addTaskBtn');
    const closeBtn = document.getElementById('closeModal');
    const saveBtn = document.getElementById('saveTaskBtn');

    addBtn.addEventListener('click', () => modal.classList.add('active'));
    closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.remove('active'); });

    saveBtn.addEventListener('click', () => {
        const title = document.getElementById('taskTitle').value;
        const subjectValue = document.getElementById('taskSubject').value;
        const subjectName = document.getElementById('taskSubject').options[document.getElementById('taskSubject').selectedIndex].text;
        const time = document.getElementById('taskTime').value;

        if (title && time) {
            let [hours, minutes] = time.split(':');
            let ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12 || 12;
            const timeStr = `${hours}:${minutes} ${ampm}`;

            initialTasks.push({
                id: Date.now(),
                title: title,
                time: timeStr,
                subject: subjectValue,
                subjectName: subjectName,
                completed: false
            });

            renderTasks();
            updateProgressCircle();
            modal.classList.remove('active');
            
            // reset inputs
            document.getElementById('taskTitle').value = '';
            document.getElementById('taskTime').value = '';
        } else {
            alert('Please fill in both task title and time.');
        }
    });

    // ---- Progress logic ----
    function updateProgressCircle() {
        const total = initialTasks.length;
        const completed = initialTasks.filter(t => t.completed).length;
        const percentage = total === 0 ? 0 : Math.round((completed / total) * 100);
        
        const circle = document.querySelector('.progress-circle circle.progress');
        const text = document.querySelector('.progress-text h2');
        
        const dashoffset = 314 - (314 * percentage) / 100;
        circle.style.strokeDashoffset = dashoffset;
        text.textContent = `${percentage}%`;
    }

    updateProgressCircle();
});
