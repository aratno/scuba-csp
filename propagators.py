#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

import itertools

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newVar=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newVar (newly instaniated variable) is an optional argument.
      if newVar is not None:
          then newVar is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newVar = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newVar = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    # IMPLEMENT
    # See algo from csc384w17-Lecture04-BTSearch.pdf p. 51

    # Return values
    has_no_deadend = True
    pruned = []

    if not newVar:
        # "If newVar is none, check all constraints" with one unasgn var
        constraints = list(filter(lambda cons: cons.get_n_unasgn() == 1, csp.get_all_cons()))
    else:
        # Only use constraints that include newVar
        constraints = list(filter(lambda cons: cons.get_n_unasgn() == 1, csp.get_cons_with_var(newVar)))
    #print('Found {} valid constraints: {}'.format(len(constraints), constraints))

    for c in constraints:
        # Check that uninit variable in c still has feasible values
        uninit_var = c.get_unasgn_vars()[0]
        #print('Using variable {} for constraint {}'.format(uninit_var, c))
        for uninit_d in uninit_var.cur_domain():
            if not c.has_support(uninit_var, uninit_d):
                uninit_var.prune_value(uninit_d)
                pruned.append((uninit_var, uninit_d))

        if uninit_var.cur_domain_size() == 0:
            has_no_deadend = False
            return has_no_deadend, pruned

    # Otherwise, return no deadend and successful prunings
    return has_no_deadend, pruned

def prop_GAC(csp, newVar=None):
    # IMPLEMENT
    # See algo from csc384w17-Lecture04-BTSearch.pdf p. 98

    # Return values
    has_no_deadend = True
    pruned = []

    # GAC queue
    q = []

    if not newVar:
        # Check all constraints
        q.extend(csp.get_all_cons())
    else:
        # Only check constraints with newVar in scope
        q.extend(csp.get_cons_with_var(newVar))

    # Initial GAC enforce
    while q:
        c = q.pop(0)
        for v in c.get_scope():
            for d in v.cur_domain():
                sat = False

                doms = []
                for aux_var in c.get_scope():
                    if aux_var == v:
                        doms.append([d])
                    else:
                        doms.append(aux_var.cur_domain())

                for vals in itertools.product(*doms):
                    if c.check(vals):
                        sat = True

                if not sat:
                    v.prune_value(d)
                    pruned.append((v, d))
                    #print(pruned)
                    if v.cur_domain_size() == 0:
                        # DWO
                        has_no_deadend = False
                        return has_no_deadend, pruned
                    else:
                        # Add next constraints to queue
                        for c in csp.get_cons_with_var(v):
                            if c not in q:
                                q.append(c)
    # No DWO found, all constraints traversed
    return has_no_deadend, pruned

