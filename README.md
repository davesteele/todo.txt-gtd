# todo.txt-gtd
My recipe for customizing a [**todo.txt**](http://todotxt.org/) environment for
[**Getting Things Done**](https://gettingthingsdone.com/).

[Installing](#Installing)

# Scripts

## The Cleanup Script

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

## The Context Listing Script

The _tdtlist_ script lists the tasks in todo.txt, by context.

If you process either of the above todo.txt files through _tdtlist_, it will output the following

    @errands
    
    Get an oil change @errands +CarMaintenance
    Get a Haircut @errands +Grooming
    
    @home
    
    Check the car battery water level @home +CarMaintenance

The list is saved in text and LibreOffice ".odt" formats. It can be optionally
automatically opened after it is created.

## The Project script

The _tdtproj_ script supports working with a single project, or group of projects. It opens an
edit session with just the specified project section from the todo.txt file, and replaces that
section after the session is complete.

If all of the lines are deleted from the edit session, no changes are made to the original
todo.txt file. If just the header line is kept, all other lines are deleted from the original.

Run _tdtproj_ with the "-l" option to get a current list of projects.

A bash completion script is available that responds to tab completion with an appropriate project
list.

## The Backup script

_tdtbackup_ is a utility script for making rotating backups of the todo.txt file.

# Working with a GTD todo.txt

Always add an '@' context to tasks, to put them on the proper GTD list, and to identify them to _tdtcleanup_.

Either add '+' project name to individual tasks, or physically move them to the appropriate Project Section.

Add comments, as necessary, to fully document each Project.

For the Weekly Review:

* Run _tdtcleanup_
* Delete completed tasks
* Update the '@~' -> '@' context on multi-step tasks as necessary
* Add tasks and '+' project tags, as needed
* Run _tdtcleanup_ again

I've found that running "``for proj in  `tdtproj -l`; do tdtproj $proj; done``" is a mind-clearing way to
accomplish this.

# Configuring Existing todo.txt Apps

Filter on '@' to limit your task lists to just tasks. I use a '\~' as a special context flag (e.g. '@\~errands') for tasks that cannot be performed yet due to an uncompleted previous step. If you pick up this convention, you may want to filter out '@~' from your lists as well.

Avoid the 'archive' operation. This typically will remove duplicate lines in _todo.txt_. This can wreak havoc on formatting, eliminating white space and empty comment lines in the file.

# Specific Todo.txt Apps for GTD

I've used the classic [todo.txt CLI](https://todotxt.org/) with success. As mentioned previously, avoid the archive operation.

I've come to prefer [ToPydo](https://pypi.org/project/topydo/), for its support
of [threshold dates and recurrance](https://github.com/mpcjanssen/simpletask-android/blob/master/app/src/main/assets/extensions.en.md). Note that it needs a [small change](https://github.com/davesteele/topydo/commit/fafee24beb4718f375a921f3b4772c5fea37d7ac) to avoid eliminating blank lines. Make sure to use the '-a' option to disable auto-archive on task completion.

[SimpleTask](https://play.google.com/store/apps/details?id=nl.mpcjanssen.todotxtholo&hl=en_US) works well on Android. Make a "Current Tasks" filter with the "List" tab consisting of a checked "Invert Filter" box, plus check "-" and all contexts you want to eliminate (e.g. "someday").

Run 'tdtlist -l' for a printable todo list, for offline use.

Of course, a primary way of interacting with the todo list is by editing the todo.txt file directly.

My .bashrc to support todo.txt:

    alias vitodo='vim ~/Dropbox/todo/todo.txt; tdtcleanup'
    alias cdtodo='cd ~/Dropbox/todo/'
    alias todo='topydo -a -t ~/Dropbox/todo/todo.txt'

And my cron:

    0 2 * * * tdtbackup; tdtcleanup; tdtlist

<a name="Installing"/>

# Installing

[Deb package](https://davesteele.github.io/todo.txt-gtd/deb/tdtgtd_0.1_all.deb)

# Usage

    $ tdtcleanup -h
    usage: tdtcleanup [-h] [-f FILE]
    
    Clean up the todo.txt file in a GTD fashion
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  the todo.txt file location (defaults to
                            ~/Dropbox/todo/todo.txt)

---

    $ tdtlist -h
    usage: tdtlist [-h] [-f FILE] [-l] [TERM [TERM ...]]
    
    List the tasks in todo.txt, by @category
    
    positional arguments:
      TERM                  search terms to filter the reported tasks
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  the todo.txt file location (defaults to
                            ~/Dropbox/todo/todo.txt)
      -l, --launch          open the task list, after creating

    Process the todo.txt file, and save tasks lists, by context, in text and
    LibreOffice formats. The lists are saved in the same directory as todo.txt.
    Optionally, the LibreOffice list can be automatically opened.

---

    $ tdtproj -h
    usage: tdtproj [-h] [-f FILE] [-l] [TERM [TERM ...]]
    
    Work with one or more GTD projects in todo.txt
    
    positional arguments:
      TERM                  search terms to filter the project(s) to use
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  the todo.txt file location (defaults to
                            ~/Dropbox/todo/todo.txt)
      -l, --list            just list the projects in the current todo.txt file

---

    $ tdtbackup -h
    usage: tdtbackup [-h] [-f FILE] [-b BACKUPDIR] [-n NUM]
    
    Back up the todo.txt todo.txt file
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  the todo.txt file location (defaults to Dropbox)
      -b BACKUPDIR, --backupdir BACKUPDIR
                            the backup location (defaults to "todo/backup" in
                            Dropbox)
      -n NUM, --num NUM     the number of backup files to keep (defaults to 14)

