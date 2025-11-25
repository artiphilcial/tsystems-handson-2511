# Exploring Evaluation Studio
This lab describes how you can use the evaluation studio to compare the performance of several prompts to select the best performing one which is then deployed into a deployment space so that it can be accessed programmatically.


# Import sample project

* To save you some time, we have created a sample project that you can use to complete this lab.

* **Download** the project zip file (evaluation_lab.zip) from this folder.

* **Save it** on your desktop or at another location you can easily find.
<!--
#<span style="color:red">
##If you prefer to create the project and prompt templates yourself, follow the instructions on 02_create_project and 03_create_prompts. 
After completing those instructions, proceed in this document to the paragraph called 
“Associate the use case with the project”.
</span>
-->

## Import the project

* From the use case screen, click **Main menu -> Projects -> right-click on View all projects**, then select **Open Link in New Tab** (or the equivalent in your browser).  
![import Project](<images/3.1.1importProject.png>)

* Go to the new browser tab that shows your list of projects. Click on the **New project** button. 
![import Project](<images/3.1.2Projects.png>)
* On the Create a project window, select **Local file** from the left-hand menu. 
![import Project](<images/3.1.3create_a_project.png>)

* Browse for and select the project zip file you just downloaded. 

- Fill in the fields
  - **Name** = “Claims summarization for Evaluation Studio”, and add your initials  
  - **Description** = “Development project for claims summarization solution”  
  - Select the appropriate storage service for your environment.  
  - Click on **Create**.
![fill in project](<images/3.1.4fill_create_a_project.png>)

* In the confirmation window, click on **View  new project**
![import Project](<images/3.1.5fill_confirmation.png>)

## Associate a watsonx.ai Runtime

- Go to the **Manage** tab, then the **Services and integration** option in the left-hand menu.
![select at sidebar: "Services & Integration" -> Manage](<images/3.2.1manage_tag_associate.png>)
- Click **Associate service** button.

- Select the appropriate watsonx.ai Runtime service in your environment, and click **Associate**.

![select "Associate Service" -> "associate"](<images/3.2.3associate_service.png>)

# Run the evaluation

## Create the evaluation experiment

* Go to the browser tab that shows your **project**

* Go to the **Assets** tab. if not already there.

* Select **New asset**
![associate workspace](<images/3.3.1new_asset.png>)

- On the **What do you want to do?** screen, search for the **Evaluate and Compare prompts** tile and click on the **Evaluate and Compare prompts** tile  
![evaluate_and_compare](<images/3.3.2evaluate_prompts_tile.png>)

- Name the experiment as **“Insurance Claim Evaluation YourInitials”**. Select the *task type* as **Summarization**. Then click on **Next**. 
![evaluate_and_compare](<images/3.3.3evaluate_and_compare.png>)

- **Select** the three prompts you imported or created earlier, then click **Next**.
![three prompts](<images/1.1_evaluate_prompts.png>)

- On the **Evaluate and compare prompts** screen, review the different metrics which you are evaluating against. These fall under the categories Generative AI Quality and Model Health and can be configured from here if needed. Click on **Next**. 
![next](<images/3.3.5generative_ai_health.png>)

- On the *Test Data* screen, click on the **Select data from project** button.
![select data](<images/3.3.6select_data.png>)

- On the *Select data* screen, select **Project file** in the left-hand column. 
![next](<images/3.3.7select_project_file.png>)
- Next, on the *Select data* screen, select **Insurance Claims Summarisation test data.csv** from the project in the second column, then click **Select**. 
![select](<images/3.3.8select_insurance_claims.png>)
- Select the **“Insurance Claim”** field as the input mapping and the **“Summary”** field as the output mapping. Then click **Next**. 
![next](<images/3.3.9select_output_mapping_summary.png>)

- Review the evaluation setup, then click **Run evaluation**. 
![run evaluation button](<images/3.3.10run_evaluation.png>)

- The evaluation run will take a few minutes to complete.
![next](<images/3.3.11evaluation_in_progresspng.png>)


Since the evaluation will take some time, you can proceed to the next step/folder (5_external-data) and continue with the deployment of the prompt template. Later, you can return to check the results of the evaluation experiment.


## Review the evaluation results  
  - You will be able to review the results.  (Note: Your results will look slightly different because we utilized some other models than what is shown in the screenshots).
  - From the metrics selection dropdown, select **Input token count**.  
  ![next](<images/3.3.11select_input_token_count.png>)

  - As you can see, the three prompts have <u>comparable input tokens metrics</u>.  
  ![next](<images/3.3.12comparable_input_tokens.png>)
  - From the metrics selection dropdown, select **Output token count**.  
  ![next](<images/3.3.14select_output_token.png>)
  - Here in the above figure, the three prompts have **more varied** results. The llama-based prompt seems to generate more tokens in general.
  - From the metrics selection dropdown, select **Content Analysis**.  
    ![next](<images/3.3.18select_content_analysis.png>)

  - The three prompts perform comparably on the **Repetitiveness** and **Coverage** metrics, but differ quite a lot on the other three metrics.  
    ![next](<images/3.3.19content_analysis_diff.png>)

  - You might have also noted that some of the bar charts have an orange dotted line. These lines represent the threshold value that was set for that metric.  
  - Hover your mouse over the threshold line in the **Repetitiveness** chart. For this metric the threshold is an *upper threshold* and is set to **0.2** – the metric needs to be at most 0.2. All three prompts stay <u>well below</u> that threshold.  
    ![next](<images/3.3.20threshold_repetitiveness.png>)

  
  - Hover your mouse over the **threshold line** in the **Coverage** chart. For this metric the threshold is a lower threshold and is set to **0.7** – the metric needs to be at least 0.7. All three prompts <u>fall short</u> of that threshold.  
      ![next](<images/3.3.21threshold_coverage.png>)

  - Spend some time going through the other metrics, identifying how each prompt performs differently across several criteria.  
  - You can also exclude a prompt to make it easier to identify the best performing prompt.  
    - **Click** on the **Assets** button on the left side of the screen.  
    - **Unselect** one of the prompts to remove it from the visualizations.  
  ![next](<images/3.3.22excluding_prompts.png>)


  - All three prompts are quite basic; in real life we would refine them to meet metric thresholds (e.g. similarity) and re-evaluate. For this lab, assume that’s done and move forward with the mistral-based prompt as our preferred candidate.  

For more information about the IBM's Evaluation Studio, please refer to the [Documentation](https://www.ibm.com/docs/en/watsonx/saas?topic=models-evaluation-studio).

