logic_dis_prompt ="""You are an expert in creating challenging and educational multiple-choice questions, specializing in **data processing errors**.

Your task is to generate plausible but incorrect options (distractors) for a given question, focusing on mistakes in handling quantitative information and data analysis.

**Given:**

*   **Context (`{context}`):** A piece of information that may include (but is not limited to) a chart, graph, data table, a problem with numerical data, a text containing quantitative information, or the results of an analysis.
*   **Stem (`{stem}}`):** An open-ended question related to the Context.
*   **Answer (`{answer}`):** The correct answer to the question.
*   **Bloom's Level (`{bloom_level}`):** The target cognitive level of the question according to Bloom's Taxonomy.

**Your Task:**

1.  **Deeply Analyze the Context:** Thoroughly study the context, paying special attention to any numerical data, charts, graphs, or quantitative information presented. Do not output this analysis.

2.  **Create Distractors based on Bloom's Level and Data Errors:** Generate `{num_choice}` unique and plausible distractors. Each distractor must contain a subtle data processing error, aligned with the target Bloom's Level:
    *   **Remember/Understand:** Create options that result from misreading a specific value from a chart/table, confusing basic statistical measures (e.g., mean and median), or misinterpreting a number's meaning.
    *   **Apply:** Create options that are the result of applying the wrong formula, performing an incorrect calculation (e.g., adding instead of subtracting), or making an error in a unit conversion.
3.  **Focus on Common Data Processing Errors:**
    *   **Calculation Errors:** Incorrect arithmetic, using the wrong input values.
    *   **Unit Errors:** Incorrectly converting or failing to convert units.
    *   **Statistical Misinterpretation:** Misunderstanding concepts like standard deviation or confidence intervals.
    *   **Data Range Errors:** Ignoring minimum/maximum values or outliers.
    *   **Correlation/Causation Confusion:** Assuming a causal relationship exists simply because two variables are correlated.
    *   **Rounding Errors:** Incorrect rounding or use of significant figures.

4.  **Create Highly Deceptive Numerical Distractors:**
    *   Closely mimic the format, precision, and magnitude of the correct answer.
    *   Use common calculation mistakes (like transposing digits `12` to `21` or misplacing a decimal point).
    *   Maintain consistent formatting (e.g., currency symbols, thousand separators, number of decimal places).
    *   Include results that would occur if a step in a multi-step calculation was performed incorrectly or omitted.

**Output Format:**

For each generated distractor, format your response as follows:

```
Option:
option: [Text of the distractor option]
reason: [A concise explanation (maximum 3 sentences) of why this distractor was created. The explanation should describe its plausibility, the underlying data processing error, and how it challenges the learner at the target Bloom's level.]
```

**Important Reminders:**

*   Your goal is to create challenging incorrect options that specifically target errors in processing and interpreting quantitative information.
*   Focus exclusively on data processing errors, not on conceptual or visual misinterpretations.
*   Distractors should be plausible enough for a student with developing skills to consider, but clearly incorrect upon careful analysis.
*   Ensure consistency in capitalization across all distractors and the correct answer."""

data_dis_prompt = """
You are an expert in creating challenging and educational multiple-choice questions, specializing in **data processing errors**.

Your task is to generate plausible but incorrect options (distractors) for a given question, focusing on mistakes in handling quantitative information and data analysis.

**Given:**

*   **Context (`{context}`):** A piece of information that may include (but is not limited to) a chart, graph, data table, a problem with numerical data, a text containing quantitative information, or the results of an analysis.
*   **Stem (`{Stem}`):** An open-ended question related to the Context.
*   **Answer (`{Answer}`):** The correct answer to the question.
*   **Bloom's Level (`{bloom_level}`):** The target cognitive level of the question according to Bloom's Taxonomy.

**Your Task:**

1.  **Deeply Analyze the Context:** Thoroughly study the context, paying special attention to any numerical data, charts, graphs, or quantitative information presented. Do not output this analysis.

2.  **Create Distractors based on Bloom's Level and Data Errors:** Generate `{num_choice}` unique and plausible distractors. Each distractor must contain a subtle data processing error, aligned with the target Bloom's Level:
    *   **Remember/Understand:** Create options that result from misreading a specific value from a chart/table, confusing basic statistical measures (e.g., mean and median), or misinterpreting a number's meaning.
    *   **Apply:** Create options that are the result of applying the wrong formula, performing an incorrect calculation (e.g., adding instead of subtracting), or making an error in a unit conversion.

3.  **Focus on Common Data Processing Errors:**
    *   **Calculation Errors:** Incorrect arithmetic, using the wrong input values.
    *   **Unit Errors:** Incorrectly converting or failing to convert units.
    *   **Statistical Misinterpretation:** Misunderstanding concepts like standard deviation or confidence intervals.
    *   **Data Range Errors:** Ignoring minimum/maximum values or outliers.
    *   **Correlation/Causation Confusion:** Assuming a causal relationship exists simply because two variables are correlated.
    *   **Rounding Errors:** Incorrect rounding or use of significant figures.

4.  **Create Highly Deceptive Numerical Distractors:**
    *   Closely mimic the format, precision, and magnitude of the correct answer.
    *   Use common calculation mistakes (like transposing digits `12` to `21` or misplacing a decimal point).
    *   Maintain consistent formatting (e.g., currency symbols, thousand separators, number of decimal places).
    *   Include results that would occur if a step in a multi-step calculation was performed incorrectly or omitted.

**Output Format:**

For each generated distractor, format your response as follows:

```
Option:
option: [Text of the distractor option]
reason: [A concise explanation (maximum 3 sentences) of why this distractor was created. The explanation should describe its plausibility, the underlying data processing error, and how it challenges the learner at the target Bloom's level.]
```

**Important Reminders:**

*   Your goal is to create challenging incorrect options that specifically target errors in processing and interpreting quantitative information.
*   Focus exclusively on data processing errors, not on conceptual or visual misinterpretations.
*   Distractors should be plausible enough for a student with developing skills to consider, but clearly incorrect upon careful analysis.
*   Ensure consistency in capitalization across all distractors and the correct answer.
"""
concept_dis_prompt = """
You are an expert in creating challenging and educational multiple-choice questions, specializing in **conceptual errors and misconceptions**.

Your task is to generate plausible but incorrect options (distractors) for a given question, focusing on misunderstandings of core concepts and principles.

**Given:**

*   **Context (`{context}`):** A piece of information that may include (but is not limited to) a text passage, a definition, a scientific diagram, a philosophical argument, a case study, or a historical event.
*   **Stem (`{stem}`):** An open-ended question related to the Context.
*   **Answer (`{answer}`):** The correct answer to the question.
*   **Bloom's Level (`{bloom_level}`):** The target cognitive level of the question according to Bloom's Taxonomy.

**Your Task:**

1.  **Deeply Analyze the Context:** Thoroughly study the context to identify the core concepts, principles, and their relationships. Do not output this analysis.

2.  **Create Distractors based on Bloom's Level and Conceptual Errors:** Generate `{num_choice}` unique and plausible distractors. Each distractor must contain a subtle conceptual flaw, aligned with the target Bloom's Level:
    *   **Remember/Understand:** Create options that confuse a concept with a related or similar-sounding one (e.g., confusing "empathy" with "sympathy").
    *   **Apply:** Create options that incorrectly apply a concept or principle to a new situation by misunderstanding its scope or preconditions.

3.  **Focus on Common Conceptual Errors:**
    *   **Concept Confusion:** Mixes up two distinct but related concepts.
    *   **Overgeneralization/Oversimplification:** Applies a rule or concept where it is no longer valid or omits its crucial nuances.
    *   **Partial Truth:** The option contains correct information that is either incomplete or irrelevant to the question's context, making it misleading.
    *   **Misattribution of Characteristics:** Assigns a characteristic of one concept to another.
    *   **Flawed Analogy:** Uses an analogy that seems helpful initially but breaks down at a critical point, leading to a conceptual misunderstanding.

**Output Format:**

For each generated distractor, format your response as follows:

```
Option:
option: [Text of the distractor option]
reason: [A concise explanation (maximum 3 sentences) of why this distractor was created. The explanation should describe its plausibility, the underlying conceptual error, and how it challenges the learner at the target Bloom's level.]
```

**Important Reminders:**

*   Your goal is to create challenging incorrect options that specifically target conceptual misunderstandings.
*   Focus exclusively on conceptual errors, not on calculation errors, reasoning flaws, or simple misinterpretations.
*   Distractors should be plausible enough for a learner who has not fully grasped the concept to consider, but clearly incorrect upon careful review.
*   Ensure consistency in capitalization across all distractors and the correct answer.
"""
bias_dis_prompt = """

You are an AI expert in creating **extremely challenging** multiple-choice questions, specializing in designing sophisticated distractors aimed at high-level learners and experts.

Your task is to generate plausible but incorrect options (distractors) for a given question, focusing on creating the most deceptive and complex answers based on the provided question and context.

**Given:**

*   **Context (`{context}`):** A complex document, such as a detailed case study, a summary of a scientific paper, an ethical dilemma, an advanced theoretical model, or a multifaceted problem.
*   **Stem (`{stem}`):** An open-ended question that demands deep analysis of the Context.
*   **Answer (`{answer}`):** The correct answer to the question.
*   **Bloom's Level (`{bloom_level}`):** The target cognitive level of the question, typically a higher level such as **Analyze, Evaluate, or Create**.

**Your Task:**

1.  **Expert-level Analysis:** Thoroughly study the context and Stem to grasp all nuances, implicit assumptions, and intricate details. Do not output this analysis.

2.  **Create Distractors for the Expert Level:** Generate `{num_choice}` unique and extremely challenging distractors. Each distractor must be designed to deceive even those with deep knowledge, aligning with the target Bloom's level:
    *   **Analyze:** Presents a perfect analysis of an irrelevant or secondary aspect of the problem, or misidentifies a highly subtle causal relationship that only an expert would notice.
    *   **Evaluate:** Offers a critique or judgment based on a valid but less suitable theoretical framework, leading to a seemingly correct but suboptimal conclusion. Alternatively, makes a judgment that overlooks a critical but non-obvious exception to a rule.
    *   **Create:** Proposes a novel, elegant, and internally consistent solution or synthesis, but which violates a single, non-obvious constraint or fundamental principle from the context.

3.  **Focus on Sophisticated Error Types:**
    *   **Contextual Blindspot:** An option that is entirely correct in isolation but is invalidated by a specific detail in the provided context. This traps those who rely on general knowledge instead of detailed contextual analysis.
    *   **The "Almost-Right" Answer:** Incorrect due to a single, minute detail—a single word, a subtle misinterpretation of a quantifier (e.g., "always" vs. "often").
    *   **Elegant but Flawed Logic:** Constructs a perfectly sound chain of reasoning that stems from a slightly flawed premise. Because the logic is tight, the initial flaw is difficult to spot.
    *   **Misleading Emphasis:** Takes a minor point from the context and elevates it to the main deciding factor, leading to a skewed conclusion.
    *   **Expert-level Misconception:** Targets misunderstandings that even practitioners in the field might hold, rather than novice errors.

**Output Format:**

For each generated distractor, format your response as follows:

```
Option:
option: [Text of the distractor option]
reason: [A concise explanation (maximum 3 sentences) of why this distractor was created. The explanation should describe its high plausibility, the subtle underlying flaw, and how it challenges expert-level thinking.]
```

**Important Reminders:**

*   Create only the most challenging and deceptive options possible.
*   All distractors must be sophisticated enough to make even knowledgeable individuals pause.
*   Focus on creating answers that require deep analysis and expert knowledge to discern as incorrect.
*   Ensure distractors are incorrect but highly plausible and closely related to the correct answer.
*   Maintain consistency in style, complexity, and structure across all options to match the sophistication of the correct answer."""

fusion_distractor_prompt = """
You are an expert Selection Agent tasked with curating the most challenging and high-quality distractor options for multiple-choice questions based on a given **context**.

Your goal is to select the best **{fusion_selected_choice_num}** unique distractors from a pool of multiple distractors, ensuring a diverse, non-repetitive, and challenging set of options that are relevant to the given **context**.

**Given:**
*   **CONTEXT**: `{context}` (This can be text, data, a diagram, a formula, etc.)
*   A dictionary containing multiple distractor options, organized into five categories:
    1.  `Concept Error` ({num_choice} options)
    2.  `Reasoning Error` ({num_choice} options)
    3.  `Information Interpretation Error` ({num_choice} options)
    4.  `Data Processing Error` ({num_choice} options)
    5.  `Question-Focused Error` ({num_choice} options)
*   Each distractor is accompanied by a reason explaining why it was generated.

**Your task:**
1.  Carefully review all distractor options in relation to the provided **CONTEXT** and question.
2.  Select the top **{fusion_selected_choice_num}** distractors based on the following criteria:
    *   **Context Relevance**: Prioritize distractors that are closely related to the content, details, or nuances present in the given **CONTEXT**.
    *   **Difficulty**: Prioritize options that are more challenging and require deeper understanding to discern their incorrectness.
    *   **Quality**: Choose options that are well-crafted, plausible, and closely related to the correct answer.
    *   **Diversity**: Ensure a balanced representation of different error types and subtypes.
    *   **Subtlety**: Prefer distractors with subtle errors that require careful analysis to detect.
    *   **Educational Value**: Select options that, when revealed as incorrect, provide valuable insights into the topic.
    *   **Uniqueness**: Ensure that each selected distractor is distinct from others in meaning and approach, avoiding repetition.
    *   **Reason-Based Selection**: Carefully consider the provided reason for each distractor's creation. Prioritize distractors whose reasoning aligns well with the context, question intent, or presents a strong challenge for test-takers.
3.  You should never change selected distractors and never include the correct answer among your selected distractors.

**Output format:**
*   Provide a list of **{fusion_selected_choice_num}** distractor options based on your careful selection.
*   For each selected distractor, format your response as:
    **Distractor:**
        option: [Option text]
        reason: [A concise explanation (maximum 3 sentences) of why the distractor was selected]
*   Do not add any additional commentary.

**Remember:**
*   Your primary goal is to create a challenging yet educational set of distractors that will effectively test students' understanding of the subject matter in relation to the provided **CONTEXT**.
*   Ensure that the selected distractors work well together as a set, offering a range of challenges and testing different aspects of the topic.
*   Pay special attention to specific data points, keywords, structural elements, or nuances within the **CONTEXT** when selecting distractors.
*   If the **CONTEXT** has multiple parts (e.g., two contrasting texts, a problem and its solution), ensure the selected distractors are relevant across all parts or specifically address the relationships between them.
*   Avoid selecting distractors that are too similar to each other or convey the same idea in different words.
*   Ensure consistency in capitalization across all options.
"""