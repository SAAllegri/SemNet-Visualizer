3D Visualizer

Video example/instructions: https://www.youtube.com/watch?v=f9L1P_2LPeA&ab_channel=StephenAllegri

What needs to be setup before it can run:

- The JS libraries should be located in the "lib" folder and referenced relatively. If it doesn't work on your end, follow the commented src below.
- The python libraries need to be installed and readable to the python interpreter. These are pretty common libraries, and all of them come in default conda.
- A python local server must be established (d3 requires it). It is extremely simple to do, here is a link to instructions: https://medium.com/@ryanblunden/create-a-http-server-with-one-command-thanks-to-python-29fcfdcd240e
	
	Simple instructions to start local python server:
	
		1. Open a command prompt in desired directory (ideally in the folder containing all of the scripts/data/etc., but doesn't have to be)
		2. Type in: python -m http.server 8000
		3. Open your browser and type in localhost:8000

- DATA MUST BE CORRECTLY FORMATTED! (look at sample data folders for example)

	Example (this must be followed precisely)- let's assume the folder containing all the scripts is named visualizer:

		Visualizer
		|
		|-json_to_3dgraph
		|-nodes_linkes_output (this won't be here if you haven't run semnet_data_to_json yet)
		|-lib
		|-semnet_data_to_json
		|-DATA (main data folder)
		    |
		    |-SN1 (first sub data folder; this will hold all information associated with SOURCE NODES)
		    |	|
		    |	|-DiseaseOrSyndrome (must be a NAMED source node type)
		    |		|
		    |		|-.xlsx1 (actual data; 3 files implies 3 target nodes)
		    |		|-.xlsx2
		    |		|-.xlsx3
		    |
		    |-SN2
		    |	|
		    |	|-DiseaseOrSyndrome
		    |	|	|
		    |	|	|-.xlsx1
		    |	|	|-.xlsx2
		    |	|
		    |	|-GeneOrGenome
		    |		|
		    |		|-.xlsx1
		    |		|-.xlsx2
		    |   
    		    |	
  		    |-SN3
		    	|
		    	|-DiseaseOrSyndrome
		    		|
		    		|-.xlsx1

- THE DATA FILES THEMSELVES MUST BE VERY SPECIFICALLY NAMED
	
	Format: INITIALS_simulation_results_Source=SOURCE-NODES_SOURCE-NODE-TYPE_Target=TARGET-CUI_TARGET-NAME
		
		- INITIALS --> initials of data owner
		- SOURCE-NODES --> The joint (A/A-B/A-B-C) number associated with each source node. This will be comprised of the CUIs of target nodes associated with 
				   source node.
		- SOURCE-NODE-TYPE --> DiseaseOrSyndrome, AminoAcidPeptideOrProtein, TherapeuticOrPreventiveMeasure, etc. what kind of source node is being evaluated.
		- TARGET-CUI --> The target CUI associated with that specific SemNet result.
		- TARGET-NAME --> The name associated with that specific SemNet result. 
	
	Example: SA_simulation_results_Source=C0002395-C0020676_DiseaseOrSyndrome_Target=C0002395_AD

	Example2: SA_simulation_results_Source=C0002395-C0020676-C0037313_DiseaseOrSyndrome_Target=C0002395_Hypothyroidism

- Any questions unanswered in this README can be sent to sallegri3@gatech.edu (this is still a work in progress, feel free to make it more efficient).

Things to be done:

- Jupyter notebook-ify
- Create legend for colored source/target nodes.
- Optimize generate_csv() and top_average_avg_hetesim() to new version of visualizer.
- Improve performance.

