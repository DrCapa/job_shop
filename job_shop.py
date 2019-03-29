"""Example for a job shop problem schedule"""

from pyomo.opt import SolverFactory
from pyomo.environ import *
import pandas as pd
import os
# Plot lib
import plotly
from plotly.offline import plot
import plotly.plotly as py
import plotly.figure_factory as ff


# Input
path_jobs = 'jobs/'
files = os.listdir(path_jobs)
data = pd.DataFrame()
colors = {'Job_1': 'rgb(220, 0, 0)', 'Job_2': 'rgb(46, 137, 205)',
          'Job_3': 'rgb(0, 255, 100)', 'Job_4': 'rgb(40, 100, 105)'}
# Read all job tickets in folder jobs
jobs = []
tasks_x_job = {}
for file in files:
    job_id = int(file.split('.')[0])
    temp = pd.read_csv(path_jobs+file)
    temp.insert(0, 'id', job_id)
    data = data.append(temp, ignore_index=True)
    jobs.append(job_id)
    tasks_x_job.update({job_id: len(temp['task'])})
temp = []
time_x_task = {}
machine_x_task = {}
for i in data.index:
    task = (int(data.loc[i, 'id']), int(data.loc[i, 'task']))
    temp.append(task)
    time_x_task.update({task: data.loc[i, 'time']})
    machine_x_task.update({task: data.loc[i, 'machine']})
print(data)

# Define Tasks with attributes
tasks = {}
for job in jobs:
    for task in range(1, tasks_x_job[job]+1):
        if(task == 1):
            tasks.update({(job, task): {'time': time_x_task[(job, task)],
                                        'machine': machine_x_task[(job, task)]}})
        else:
            tasks.update({(job, task): {'time': time_x_task[(job, task)],
                                        'machine': machine_x_task[(job, task)],
                                        'previous': task-1}})

# Select solver
opt = SolverFactory('cbc')

# Create model
m = AbstractModel()

horizon = sum([tasks[(i, j)]['time'] for (i, j) in tasks.keys()])
machines = set(data['machine'])
m.all_tasks = Set(dimen=2, initialize=tasks.keys(), ordered=True)

m.makespan = Var(within=NonNegativeReals)
m.start = Var(m.all_tasks, machines, within=NonNegativeReals)
m.binary = Var(m.all_tasks, m.all_tasks, machines, within=Boolean)


# Objective function
def obj_expression(m):
    return m.makespan
m.obj = Objective(rule=obj_expression, sense=minimize)


# Every task has to be done in the given time
def do_tasks(m, i, j, k):
    if(k in tasks[(i, j)]['machine']):
        return m.start[(i, j), k] + tasks[(i, j)]['time'] <= m.makespan
    else:
        return Constraint.Skip
m.do_task = Constraint(m.all_tasks, machines, rule=do_tasks)


# Previous task must be done bevor starting the next
def previous_task(m, i, j, k):
    if('previous' in tasks[(i, j)] and k in tasks[(i, j)]['machine']):
        return (m.start[(i, j), k] >= m.start[(i, j-1), tasks[(i, j-1)]['machine']] +
                tasks[(i, j-1)]['time'])
    else:
        return Constraint.Skip
m.previous_task = Constraint(m.all_tasks, machines, rule=previous_task)


# No overlapping tasks for machines
def const_1(m, i1, j1, i2, j2, k):
    if(i1 < i2 and k in tasks[(i1, j1)]['machine'] and
       k in tasks[(i2, j2)]['machine']):
        return (m.start[(i1, j1, k)] + tasks[(i1, j1)]['time'] <=
                m.start[(i2, j2, k)] +
                horizon*(1-m.binary[(i1, j1), (i2, j2), k]))
    else:
        return Constraint.Skip
m.const_1 = Constraint(m.all_tasks, m.all_tasks, machines, rule=const_1)


def const_2(m, i1, j1, i2, j2, k):
    if(i1 < i2 and k in tasks[(i1, j1)]['machine'] and
       k in tasks[(i2, j2)]['machine']):
        return (m.start[(i2, j2, k)] + tasks[(i2, j2)]['time'] <=
                m.start[(i1, j1, k)] +
                horizon*(m.binary[(i1, j1), (i2, j2), k]))
    else:
        return Constraint.Skip
m.const_2 = Constraint(m.all_tasks, m.all_tasks, machines, rule=const_2)


# Create instanz
instance = m.create_instance()

# Solve the optimization problem
results = opt.solve(instance, symbolic_solver_labels=True, tee=True,
                    load_solutions=True)

# Show result
print('makespan: ', instance.makespan.value)

# Plot Gantt chart
df = []
for task in tasks:
    start = instance.start[task, tasks[task]['machine']].value
    finish = start+int(tasks[task]['time'])
    df.append(dict(Task=tasks[task]['machine'],
                   Start=start,
                   Finish=finish,
                   Resource='Job_'+str(task[0])))

fig = ff.create_gantt(df, title='Job Shop', colors=colors,
                      showgrid_x=True, showgrid_y=True, index_col='Resource',
                      show_colorbar=True, group_tasks=True)
fig['layout']['xaxis'].update({'type': None})
fig['layout']['xaxis'].update({'title': 'time'})
fig['layout']['yaxis'].update({'title': 'machine'})
fig['layout']['xaxis'].update({'range': [-1, 17]})
fig['layout']['yaxis'].update({'range': [-0.5, 2.5]})
fig["layout"].update(autosize=True)
plot(fig, filename='job_shop', image="png",
     image_filename="job_shop", auto_open=True)
