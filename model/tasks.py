from datetime import datetime
from __init__ import db, app

datecreated = datetime(2022, 11, 12)  #sample datetime for tester data
class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(255), unique=False,  nullable=True)   #I declare all of the columns, most of them are strings/integers
    priority = db.Column(db.String(255), unique=False, nullable=True)
    comments = db.Column(db.String(255), unique=False, nullable=True)
    datecreated = db.Column(db.DateTime, unique=False, default=datetime.utcnow, nullable=True)  #datetime is a unique data type, saves even the seconds at which the task was created
    order = db.Column(db.Integer, unique=False, nullable=False, default=0)  

    def __init__(self, taskname, priority, comments, datecreated, order=0): #Default order is set to 0, so tasks start off as the first thing in the table when created
        self.taskname = taskname
        self.priority = priority
        self.comments = comments
        self.datecreated = datecreated
        self.order = order 

    def read(self):
        return {   #read method, to process the information
            'id': self.id,
            'taskname': self.taskname,
            'priority': self.priority,
            'comments': self.comments,
            'datecreated': self.datecreated.strftime('%Y-%m-%d %H:%M:%S'),
            'order': self.order  
        }
    
    def create(self):   #define create method, add task and then commit the change
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod                      #This is necessary to update the order numbers in the table
    def update_task_order(new_order):
        for index, task_id in enumerate(new_order, start=1):
            task = Task.query.get(task_id)
            task.order = index
        db.session.commit()
            
def initTasks():
    with app.app_context():   #Tester data to start off the database. 
        db.create_all()  #We need to use the create method on each of these so that they are added to the database.
        t1 = Task(taskname="Do the Dishes", priority='Low', comments='Do this last, homework is more important', datecreated=datecreated, order=1)
        t2 = Task(taskname="Finish Calculus Homework", priority='High', comments='This is very important because of the test I have next week', datecreated=datecreated, order=2)
        t3 = Task(taskname="Walk the Dog", priority='Medium', comments='It is getting late, need to do this before it gets dark', datecreated=datecreated, order=3)

        tasks = [t1, t2, t3]
        for task in tasks:
            try:
                task.create()   #similar to the previous comment
            except Exception as e:
                print(f"Error creating task: {e}")
                db.session.rollback()
