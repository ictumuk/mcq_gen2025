code_prompt = """You are an expert in educational design. Your core task is to produce **detailed analytical narratives** that serve as high-quality **contexts** for future multiple-choice questions. You must deeply analyze the provided materials to generate these narratives.

**Crucial Directive: The final context you produce IS NOT a question or a command to analyze. The context IS THE ANALYSIS ITSELF, written out in full.**

**All final contexts must be written in Vietnamese.**

**Inputs:**

1.  **LECTURE_CONTENT:**
    ```text
    {text}
    ```
2.  **SUBJECT_TOPIC:** `{subject} - {topic}`
3.  **KEY_POINT:** `{key_point}`
4.  **SOLVED_EXERCISES (if any):**
    ```text
    {{exercises}}
    ```
5.  **BLOOM_LEVEL:** `{bloom_level}`
6.  **NUM_CONTEXTS:** `{number_context}`

**Detailed Task:**

Execute the following "Chain-of-Thought" process. Remember, the goal of this process is to generate material for the final written analysis.

**Hardness-first directive:** Identify the hardest, most error-prone concepts/edge cases first. Your contexts should prioritize challenging scenarios that still align with the target Bloom level, instead of starting from the easiest examples at that level.

**Step 1: Identify and Preserve Relevant Information**
   - Thoroughly review all provided content.
   - Extract and preserve the **exact, verbatim** text of all relevant definitions, code blocks, examples, and exercises. These will be included in the final context.

**Step 2: Orient Analysis**
   - Note the `BLOOM_LEVEL`. The depth and type of your analysis should reflect this level. For any level, the output must be a rich analysis.

**Step 3: In-depth Analysis of Lecture Content**
   *   **Analyze Concepts:** For each concept, analyze its core principles, edge cases, and common misconceptions.
   *   **Analyze Examples/Code:**
        *   Preserve the original example.
        *   **Perform a step-by-step trace:** Analyze the program's flow, the purpose of each line, and how variable values change.
        *   **Simulate with different inputs:** Actively consider new inputs (e.g., boundary values, zero, negative numbers). Analyze how these different inputs affect the execution flow and the final output.
        *   **Analyze for improvements/flaws:** Analyze the code for efficiency, correctness, and potential logical errors.

**Step 4: In-depth Analysis of Solved Exercises**
   *   Preserve the original problem and solution.
   *   **Analyze the given solution:** Break it down and analyze the logic and theoretical basis for each step.
   *   **Analyze alternative/flawed approaches:** Based on the correct solution, analyze common mistakes a student might make. This analysis of flawed logic is excellent material for the final context.

**Step 5: Create Contexts (Analytical Narratives)**

   *   Based on your detailed analysis in the steps above, generate `{{number_context}}` unique, high-quality analytical narratives.
   *   **Requirements for each context:**
        *   **The Nature of the Context: It IS the Analysis.** The context itself must be the complete, written-out analysis. It should read like an expert's explanation or walkthrough.
        *   **Multi-faceted Analysis:** Your analysis is not limited to the provided examples. You are encouraged to **present a scenario with modified parameters or inputs**, then **provide a step-by-step trace** of the execution with these new inputs, explaining the state of variables and the outcome at each stage.
        *   **Example of what to do and what NOT to do:**
            *   `**INCORRECT Context (Merely a command):**`
                "Đoạn mã A: [code] Đoạn mã B: [code]. Phân tích sự khác biệt về kết quả đầu ra khi thực thi Đoạn mã A và Đoạn mã B."
            *   `**CORRECT Context (The analysis itself, like the user's desired example):**`
                "Xét hai cấu trúc lặp `while` và `do-while` qua hai đoạn mã sau. **Đoạn mã A:** [code]. Trong đoạn mã này, biến `i` được khởi tạo bằng 5. Vòng lặp `while` kiểm tra điều kiện `i < 5` *trước khi* thực thi. Vì 5 không nhỏ hơn 5, điều kiện này ngay lập tức sai. Do đó, khối lệnh bên trong vòng lặp `while` không được thực thi dù chỉ một lần, và chương trình in ra 'Ket thuc while, i = 5'. **Ngược lại, trong Đoạn mã B:** [code], cấu trúc `do-while` thực thi khối lệnh *ít nhất một lần* rồi mới kiểm tra điều kiện. Vì vậy, chương trình sẽ in ra 'Gia tri cua j trong do-while: 5', sau đó tăng `j` lên 6. Lúc này, điều kiện `j < 5` (tức là 6 < 5) được kiểm tra và cho kết quả sai, vòng lặp kết thúc. Kết quả cuối cùng là 'Ket thuc do-while, j = 6'. Sự khác biệt căn bản này đến từ việc `while` là vòng lặp kiểm tra trước (pre-test loop), còn `do-while` là vòng lặp kiểm tra sau (post-test loop)."
        *   **Language and Terminology:** Write in professional **Vietnamese**. Keep standard technical terms (e.g., `for`, `while`, function names, variable names) in their **original English form**.
        *   **Integrity of Original Content:** You **MUST** include the original, unchanged text/code/example verbatim within your analytical narrative.
        *   **No Questions:** The narrative **MUST NOT** end with a question or a question mark.

**Output Format:**

For each generated context, strictly adhere to the following structure:

contexts: [An analytical narrative written **in Vietnamese**, which includes preserved original content, detailed step-by-step traces, analysis of different scenarios, and adheres to all requirements above. It **must not** contain any questions.]

Please begin your analysis and context generation.
"""

ctx_prompt = """You are an expert in educational design. Your core task is to produce **detailed analytical narratives** that serve as high-quality **contexts** for future multiple-choice questions. You must deeply analyze the provided materials from any academic subject to generate these narratives.

**Crucial Directive: The final context you produce IS NOT a question or a command to analyze. The context IS THE ANALYSIS ITSELF, written out in full, like an expert's explanation.**

**All final contexts must be written in Vietnamese.**

**Inputs:**

1.  **LECTURE_CONTENT:**
    ```text
    {text}
    ```
2.  **SUBJECT_TOPIC:** `{subject} - {topic}`
3.  **KEY_POINT:** `{key_point}`
4.  **SOLVED_EXERCISES (or Worked Examples, Case Studies):**
    ```text
    {{exercises}}
    ```
5.  **BLOOM_LEVEL:** `{bloom_level}`
6.  **NUM_CONTEXTS:** `{number_context}`

**Detailed Task:**

Execute the following "Chain-of-Thought" process. The goal is to generate rich material for the final written analysis.

**Hardness-first directive:** Identify the hardest, most error-prone concepts/edge cases first. Prioritize challenging scenarios that still align with the target Bloom level instead of starting from the easiest examples at that level.

**Step 1: Identify and Preserve Relevant Information**
   - Thoroughly review all provided content.
   - Extract and preserve the **exact, verbatim** text of all relevant **Core Objects**. A "Core Object" can be a definition, a mathematical formula, a chemical equation, a historical document excerpt, a legal clause, a philosophical argument, a diagram of a biological process, etc.

**Step 2: Orient Analysis**
   - Note the `BLOOM_LEVEL`. The depth and type of your analysis must reflect this level. For any level, the output must be a rich analysis.

**Step 3: In-depth Analysis of Lecture Content**
   *   **Analyze Concepts:** For each concept, analyze its core principles, scope of application, boundary conditions, edge cases, and common misconceptions.
   *   **Analyze Core Objects (e.g., Examples, Formulas, Diagrams):**
        *   Preserve the original Core Object.
        *   **Perform a step-by-step deconstruction or application:** Analyze the object's components, the logic of its structure, or the process of its application.
        *   **Simulate with different parameters, conditions, or assumptions:** Actively consider new scenarios. For example: How does a formula behave with different input values? How does a historical event's interpretation change with a different perspective? How does a biological process react to a change in environment? Analyze how these modifications affect the process and outcome.
        *   **Analyze for validity, efficiency, or underlying biases:** Analyze the object for its logical consistency, elegance, potential errors, or the perspective it implicitly represents.

**Step 4: In-depth Analysis of Solved Problems/Case Studies**
   *   Preserve the original problem and solution/analysis.
   *   **Analyze the provided solution:** Break it down and analyze the reasoning, evidence, or theoretical principles used in each step.
   *   **Analyze alternative/flawed approaches:** Based on the correct solution, analyze common mistakes a student might make (e.g., misinterpreting a formula, a logical fallacy in an argument, a factual error in a historical analysis). This analysis of flawed reasoning is excellent material for the final context.

**Step 5: Create Contexts (Analytical Narratives)**

   *   Based on your detailed, multi-faceted analysis, generate `{{number_context}}` unique analytical narratives.
   *   **Requirements for each context:**
        *   **The Nature of the Context: It IS the Analysis.** The context must be the complete, written-out analysis itself. It should read like a passage from a textbook or an expert's detailed explanation.
        *   **Multi-faceted and Proactive Analysis:** Your analysis is not limited to what is explicitly provided. You are **required** to present scenarios with **modified parameters, initial conditions, or assumptions**, and then **provide a step-by-step walkthrough** of the reasoning process, explaining how the components interact and how the outcome is determined under these new conditions.
        *   **Example of what to do and what NOT to do (Generalized Example - Math):**
            *   `**INCORRECT Context (Merely a command):**`
                "Đây là công thức nghiệm của phương trình bậc hai: [x = (-b ± √(b²-4ac)) / 2a]. Phân tích cách áp dụng công thức này cho phương trình 2x² + 5x - 3 = 0."
            *   `**CORRECT Context (The analysis itself):**`
                "Xét phương trình bậc hai 2x² + 5x - 3 = 0. Để giải, ta áp dụng công thức nghiệm tổng quát: [x = (-b ± √(b²-4ac)) / 2a]. Đầu tiên, ta **phân tích và xác định** các hệ số: a = 2, b = 5, và c = -3. Một lỗi thường gặp là bỏ qua dấu âm của hệ số c. Tiếp theo, ta **phân tích** biệt thức delta, Δ = b² - 4ac, là thành phần quyết định số nghiệm của phương trình. Thay số, ta có Δ = 5² - 4(2)(-3) = 25 - (-24) = 49. Vì Δ > 0, ta kết luận phương trình có hai nghiệm thực phân biệt. Nếu Δ = 0, phương trình sẽ có nghiệm kép, và nếu Δ < 0, phương trình sẽ không có nghiệm thực. Cuối cùng, ta áp dụng công thức để tìm nghiệm: x₁,₂ = (-5 ± √49) / (2*2) = (-5 ± 7) / 4. Từ đó ta có hai nghiệm là x₁ = 2/4 = 0.5 và x₂ = -12/4 = -3."
        *   **Language and Terminology:** Write in professional **Vietnamese**. Keep universally recognized technical terms, names, and formulas (e.g., `Newton`, `H₂O`, `E=mc²`, `for`, `while`) in their **original form**.
        *   **Integrity of Original Content:** You **MUST** include the original, unchanged Core Object (formula, definition, text excerpt, etc.) verbatim within your analytical narrative.
        *   **No Questions:** The narrative **MUST NOT** end with a question or a question mark.

**Output Format:**

For each generated context, strictly adhere to the following structure:

contexts: [An analytical narrative written **in Vietnamese**, which includes preserved original content, detailed step-by-step deconstruction, analysis of different scenarios, and adheres to all requirements above. It **must not** contain any questions.]

Please begin your analysis and context generation.
"""

