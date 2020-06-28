=====
Usage
=====

To use sitdown in a project:

Download mutations file
-----------------------
Currently this library only reader ABN Amro mutation downloads.

* Log in to abnamro.nl > `Zelf regelen` -> `Bij- en afschrijvingen downloaden`
* Download format TXT. Multiple accounts can be selected, sitdown can separate them later

Load Mutations file
-------------------
Suppose for this example that you downloaded the mutations file to `/TXTMutations.TAB` and that
it contains 100 mutations

In python::

    from sitdown.readers import ABNAMROReader
    mutations = ABNAMROReader().read('/TXTMutations.TAB')  #  parse all mutations

    >>> mutations  # now this contains 100 Mutation objects
    Set: 100

    >>> mutation = mutations.pop()  # get the first one from set
    >>> mutation.date
    {date} 2019-12-09

    >>> mutation.amount
    {float} -12.95

    >>> mutations.description
    {str} 'Tonys lunch room, thank you for you purchase'

    >>> mutations = list(mutations).sort()   # by default, sorts by date, oldest date first

