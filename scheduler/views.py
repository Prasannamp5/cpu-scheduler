from django.shortcuts import render, redirect
from .models import ProcessHistory

# FCFS
def fcfs(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    total = 0

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        p['waiting'] = time - p['arrival']
        total += p['waiting']
        time += p['burst']

    return processes, total / len(processes)


# SJF
def sjf(processes):
    processes = sorted(processes, key=lambda x: x['burst'])
    time = 0
    total = 0

    for p in processes:
        p['waiting'] = time
        total += p['waiting']
        time += p['burst']

    return processes, total / len(processes)


# Round Robin
def round_robin(processes, quantum):
    queue = processes.copy()
    time = 0
    total = 0

    for p in queue:
        p['remaining'] = p['burst']

    while True:
        done = True
        for p in queue:
            if p['remaining'] > 0:
                done = False
                if p['remaining'] > quantum:
                    time += quantum
                    p['remaining'] -= quantum
                else:
                    time += p['remaining']
                    p['waiting'] = time - p['burst']
                    total += p['waiting']
                    p['remaining'] = 0
        if done:
            break

    return queue, total / len(queue)


def home(request):
    return render(request, 'home.html')


def calculate(request):
    if request.method == 'POST':
        arrival = list(map(int, request.POST.getlist('arrival')))
        burst = list(map(int, request.POST.getlist('burst')))
        quantum = int(request.POST['quantum'])

        processes = []
        for i in range(3):
            processes.append({
                'id': i + 1,
                'arrival': arrival[i],
                'burst': burst[i]
            })

        fcfs_res, fcfs_avg = fcfs(processes.copy())
        sjf_res, sjf_avg = sjf(processes.copy())
        rr_res, rr_avg = round_robin(processes.copy(), quantum)

        best = min({
            "FCFS": fcfs_avg,
            "SJF": sjf_avg,
            "Round Robin": rr_avg
        }, key=lambda x: {
            "FCFS": fcfs_avg,
            "SJF": sjf_avg,
            "Round Robin": rr_avg
        }[x])

        # SAVE HISTORY
        ProcessHistory.objects.create(
            arrival=" ".join(map(str, arrival)),
            burst=" ".join(map(str, burst)),
            quantum=quantum,
            fcfs_avg=fcfs_avg,
            sjf_avg=sjf_avg,
            rr_avg=rr_avg,
            best_algo=best
        )

        return render(request, 'result.html', {
            'fcfs': fcfs_res, 'fcfs_avg': fcfs_avg,
            'sjf': sjf_res, 'sjf_avg': sjf_avg,
            'rr': rr_res, 'rr_avg': rr_avg,
            'best': best
        })


def history(request):
    data = ProcessHistory.objects.all().order_by('-created_at')
    return render(request, 'history.html', {'data': data})


def clear_history(request):
    ProcessHistory.objects.all().delete()
    return redirect('history')