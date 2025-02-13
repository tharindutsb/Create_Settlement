def get_drc_summary(Processed_case_list,distributed_DRC) :
   # Calculated DRC wise distribution count
   drc_cnt_summary = distributed_DRC.copy()
   for key in distributed_DRC:
      drc_cnt_summary[key] = 0

   for case_id in Processed_case_list:
      case_infor = Processed_case_list[case_id]
      drs_id = case_infor[0]
      exist_count = drc_cnt_summary[drs_id]
      drc_cnt_summary[drs_id] = exist_count + 1
   
   return drc_cnt_summary


def case_distribution(Planning_Case_list,distributed_DRC,drc_rtom_mapping):
   """ 
   Purpose : Allocate Cases among the DRCs
   Condition : Case Distribution should be do according to the ratio w.r.t. DRCs

   Parameters  : 
         I/P
            - Planning_Case_list (tuple) : Planning to distribute case list
            - distributed_DRC (dict) : List contains DRC and the count of distribution
            - drc_rtom_mapping (dict) : List of DRCs and its RTOMs

         O/P
            - Processed_case_list (dict) : List of cases which are distributed to DRCs
            - Processed_reject_list (tuple) : List of cases which are rejected from distribution

   Example Usage :
      - Processed_case_list,Processed_reject_list = case_distribution(Planning_Case_list,distributed_DRC,drc_rtom_mapping)
      I/P :
         - Planning_Case_list : [(1, 'CW'), (2, 'GP'), (3, 'CW'), (4, 'CW'), (5, 'AD'), (6, 'AG'), (7, 'CW'), (8, 'AG'), (9, 'KD'), (10, 'XX'), (11, 'YY'), (12, 'ww')]
         - distributed_DRC : {"D1": 4, "D2": 8, "D3": 12}
         - drc_rtom_mapping :  {
                                 "D1": ["AD", "GP", "CW"],
                                 "D2": ["AD", "AG"],
                                 "D3": ["CW", "GP", "AD"],
                               }
      O/P :
         - Processed_case_list : {1: ['D1', 'CW'], 2: ['D3', 'GP'], 3: ['D1', 'CW'], 5: ['D2', 'AD'], 4: ['D3', 'CW'], 7: ['D1', 'CW'], 6: ['D2', 'AG'], 8: ['D2', 'AG']}
         - Processed_reject_list : [(9, 'KD'), (10, 'XX'), (11, 'YY'), (12, 'ww')]

   ********* Important Valiables ************
   * Current_processing_cycle - obtain cases from the case distribution list length should be DRCs count.
   * Current_reject_cycle - reject cases from current processing cycle
   * Permenant_Reject_Case - Whole Rejected list after several cycles (Itteration).

   """
   Processed_case_list = {}
   Processed_reject_list = []

   Selected_DRC_count = len(distributed_DRC)


   Case_List_In_Current_Cycle = [None] * Selected_DRC_count
   # Current_processing_cycle
   Current_reject_cycle  = []
   Permenant_Reject_Case  = []


   i=0
   point_elemnt = 0
   for planning_case in Planning_Case_list:
      # print(planning_case)
      Case_List_In_Current_Cycle[i] = planning_case
      i = i + 1
      point_elemnt += 1

      if (i == Selected_DRC_count) or (point_elemnt == len(Planning_Case_list)) :
         # Fill cases into Case_List_In_Current_Cycle for a cycle (itteration)
         # Size of the Case_List_In_Current_Cycle is count of DRCs
         # for New cycle fill rejected cases and raming will fill from the New cases in Planning_Case_list


         print('Prepared Case_List_In_Current_Cycle {}'.format(Case_List_In_Current_Cycle))

         # Call assign_case_in_current_cycle
         Current_processing_cycle, Current_reject_cycle, Permenant_Reject_Case = assign_case_in_current_cycle(Case_List_In_Current_Cycle,drc_rtom_mapping,distributed_DRC)
         
         # Collect all cases collects from a cycle and put them into Processed_case_list(O/P)
         if len(Current_processing_cycle) > 0 :
            for drc_id in Current_processing_cycle:
               if Current_processing_cycle[drc_id] is not None :
                  case_infor = [drc_id,Current_processing_cycle[drc_id][1]]
                  Processed_case_list[Current_processing_cycle[drc_id][0]] = case_infor

         # Filter out None values -- Remove None
         filtered_list = [item for item in Permenant_Reject_Case if item is not None]
         Permenant_Reject_Case = filtered_list

         # Collect all rejected cases collects from a cycle and put them into Processed_reject_list(O/P)
         if len(Permenant_Reject_Case) > 0 :
            Processed_reject_list = Processed_reject_list + Permenant_Reject_Case

         # Re-fill cases for a new cycle
         # First Part - Fill cases rejected cases (Only fist time cases)
         Case_List_In_Current_Cycle = [None] * Selected_DRC_count
         i=0
         for slt_case_cycle_reject in Current_reject_cycle:
            Case_List_In_Current_Cycle[i] = slt_case_cycle_reject
            i = i + 1

   """
   * After complete the all Cases, there could be cases in Current_reject_cycle - first time reject also
   * should put them into Processed_reject_list
   """
   if Current_reject_cycle:
      Processed_reject_list.append(Current_reject_cycle)

   # Remove None elements if any
   Processed_reject_list = [sublist for sublist in Processed_reject_list if sublist and any(item is not None for item in sublist)]

   # Get DRCs wise distribution summary
   distributed_DRC = get_drc_summary(Processed_case_list,distributed_DRC)

   print('Process completed {}'.format(Processed_case_list))
   print('Rejected completed {}'.format(Processed_reject_list))
   print('Processed DRC wise summary {}'.format(distributed_DRC))

def check_drc_can_effort_rtom(Case_Details,drc_rtom_mapping,drc_id) :
   if not Case_Details :
      return False
   
   if Case_Details[1] in drc_rtom_mapping[drc_id]:
      # print('{} in {}'.format(Case_Details[1], drc_rtom_mapping[drc_id]))
      return True
   return False



def assign_case_in_current_cycle(Case_List_In_Current_Cycle,drc_rtom_mapping,distributed_DRC) :
   
   # I/P :
   #     Case_List_In_Current_Cycle : Get All assining List
   #     drc_rtom_mapping : List DRCs along with RTOMs can handle
   #     distributed_DRC : List DRCs along with maximum allow cases
   # O/P :
   #     Current_processing_cycle : Successfully allocated cases in current cycle
   #     Case_List_In_Current_Cycle : Rejected cases in current cycle
   #     Permenant_Reject_Case : Permenatly Rejected cases in current cycle
    
   Permenant_Reject_Case =[]

   # Create empty Current_processing_cycle; key as DRC_ID
   Current_processing_cycle = distributed_DRC.copy()
   for key in distributed_DRC:
      Current_processing_cycle[key] = None

   # Allocate Null possition only
   is_found_atlease = False
   for slt_case in Case_List_In_Current_Cycle:
      for key_drc_id in distributed_DRC:
         if Current_processing_cycle[key_drc_id] is None :
            max_able_count = distributed_DRC[key_drc_id]

            if check_drc_can_effort_rtom(slt_case,drc_rtom_mapping,key_drc_id) and max_able_count > 0:
               Current_processing_cycle[key_drc_id] = slt_case
               # New Item added, deduct by 1 from able case count of DRC
               max_able_count -= 1
               distributed_DRC[key_drc_id] = max_able_count
               is_found_atlease = True
               break
      
      if is_found_atlease is False :
         Permenant_Reject_Case.append(slt_case)

   # print('Cycle Empty completed {}'.format(Current_processing_cycle))

   # Remove Already allocated elements
   if len(Current_processing_cycle) > 0 :
      for key_cur_drc_id in Current_processing_cycle:
         if Current_processing_cycle[key_cur_drc_id] is not None :
            slt_case = Current_processing_cycle[key_cur_drc_id]
            Case_List_In_Current_Cycle.remove(slt_case)

   # Remove Permenantly Rejected Case elements
   if len(Permenant_Reject_Case) > 0 :
      for key_rej_drc_id in Permenant_Reject_Case:
         if key_rej_drc_id is not None :
            if slt_case in Case_List_In_Current_Cycle:
               Case_List_In_Current_Cycle.remove(key_rej_drc_id)

   # Try to swap if possible
   drc_id_empty = None
   for slt_case in Case_List_In_Current_Cycle:
      # Identify Empty Element
      for key_drc_id_empty in Current_processing_cycle:
         if Current_processing_cycle[key_drc_id_empty] is None :
            drc_id_empty = key_drc_id_empty
            break

      if drc_id_empty is not None :
         max_able_drc_empty_count = distributed_DRC[drc_id_empty]
         if max_able_drc_empty_count <= 0 :
            # Already quota exceed
            drc_id_empty = None

      if drc_id_empty is not None :
         # Found Empty Element
         for key_drc_id_filled in Current_processing_cycle:
            # Going to check already filled elements
            if Current_processing_cycle[key_drc_id_filled] is not None :
               slt_case_swapping = Current_processing_cycle[key_drc_id_filled]

               # Check Not Yet allocated case with already allocated DRC
               # AND
               # Check allocated case with NOT allocated DRC

               if check_drc_can_effort_rtom(slt_case,drc_rtom_mapping,key_drc_id_filled) :
                  if check_drc_can_effort_rtom(slt_case_swapping,drc_rtom_mapping,drc_id_empty) :
                     # Can Swap 
                     # NOT allocated case assiged to allocated DRC 
                     Current_processing_cycle[key_drc_id_filled] = slt_case
                     #  Allocated case assiged to NOT allocated DRC
                     Current_processing_cycle[drc_id_empty] = slt_case_swapping

                     # New Item added, deduct by 1 from able case count of DRC
                     max_able_drc_empty_count -= 1
                     distributed_DRC[drc_id_empty] = max_able_drc_empty_count
                     break

   # Remove Already allocated elements
   for key_drc_id in Current_processing_cycle:
      if Current_processing_cycle[key_drc_id] is not None :
         slt_case = Current_processing_cycle[key_drc_id]
         if slt_case in Case_List_In_Current_Cycle:
            Case_List_In_Current_Cycle.remove(slt_case)
   
   print('Cycle completed {}'.format(Current_processing_cycle))
   print('Cycle completed Reject Tem {}'.format(Case_List_In_Current_Cycle))
   print('Cycle completed Reject Per {}'.format(Permenant_Reject_Case))
   
   return Current_processing_cycle,Case_List_In_Current_Cycle, Permenant_Reject_Case






if __name__ == "__main__":
   # cases = [(1, 'CW'), (2, 'AD'), (3, 'AG'), (4, 'CW'), (5, 'GP'), (6, 'CW'), (7, 'CW'), (8, 'AG'), (9, 'KD')]
   cases = [(1, 'CW'), (2, 'GP'), (3, 'CW'), (4, 'CW'), (5, 'AD'), (6, 'AG'), (7, 'CW'), (8, 'AG'), (9, 'KD'), (10, 'XX'), (11, 'YY'), (12, 'WW')]
   distributed_DRC = {"D1": 4, "D2": 8, "D3": 12,"D4":10}
   drc_rtom_mapping = {
      "D1": ["AD", "GP", "CW"],
      "D2": ["AD", "AG"],
      "D3": ["CW", "GP", "AD"],
      "D4": ["XX","YY","WW"]
   }
   case_distribution(cases,distributed_DRC,drc_rtom_mapping)
