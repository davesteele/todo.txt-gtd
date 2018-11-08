# todo.txt-gtd
My recipe for customizing a [**todo.txt**](http://todotxt.org/) environment for
[**Getting Things Done**](https://gettingthingsdone.com/).

# The Cleanup Script

Given the following text in the file _~/Dropbox/todo/todo.txt_:

    Get an oil change @errands +CarMaintenance
    Get a Haircut @errands +Grooming
    Check the car battery water level @home +CarMaintenance

... running the _tdtcleanup_ script will convert that file to this:


    # CarMaintenance
    #
    
    Get an oil change @errands +CarMaintenance
    Check the car battery water level @home +CarMaintenance
    
    # Grooming
    #
    
    Get a Haircut @errands +Grooming
    
    # _None
    #
    

Now _todo.txt_ can be treated as a comprehensive Projects file. Tasks are
organized by Project, and arbitrary text related to projects can be added
as comments.

A '#' comment consisting of a single word is a Project Header, defining the
default project for following tasks. The final *_None* project is special -
it collects tasks that are added using various **todo.txt** applications.

On subsequent runs, _tdtcleanup_ will do the following:

* Sort Project Sections alphabetically, by Project Name
* Add the '+' project tag to any tasks in a Project Section that don't already have one. A task is defined here as a line of text that includes an '@' context. This processing doesn't happen in the *_None* section.
* Move tasks to the proper Project Section, if they aren't already there. The Section is created, using a Project Header, if necessary.

_tdtbackup_ is a utility script for making rotating backups of the todo.txt file.

# Working with a GTD todo.txt

Always add an '@' context to tasks, to put them on the proper GTD list, and to identify them to _tdtcleanup_.

Either add '+' project name to individual tasks, or physically move them to the appropriate Project Section.

Add comments, as necessary, to fully document each Project.

For the Weekly Review:

* Run _tdtcleanup_
* Delete completed tasks
* Update the '@' context on multi-step tasks as necessary
* Add tasks and '+' project tags, as needed
* Run _tdtcleanup_ again

# Configuring Existing todo.txt Apps

Filter on '@' to limit your task lists to just tasks. I use _@pending_ as a special context for tasks that cannot be performed yet due to an uncompleted previous step. If you pick up this convention, filter out _@pending_ from your lists as well.

Avoid the 'archive' operation. This typically will remove duplicate lines in _todo.txt_. This can wreak havoc on formatting, eliminating white space and empty comment lines in the file.

# Usage

    $ ./tdtcleanup -h
    usage: tdtcleanup [-h] [-f FILE]
    
    Clean up the todo.txt file in a GTD fashion
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  the todo.txt file location (defaults to
                            ~/Dropbox/todo/todo.txt)



    $ ./tdtbackup -h
    usage: tdtbackup [-h] [-f FILE] [-b BACKUPDIR] [-n NUM]
    
    Back up the todo.txt todo.txt file
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  the todo.txt file location (defaults to Dropbox)
      -b BACKUPDIR, --backupdir BACKUPDIR
                            the backup location (defaults to "todo/backup" in
                            Dropbox)
      -n NUM, --num NUM     the number of backup files to keep (defaults to 14)

