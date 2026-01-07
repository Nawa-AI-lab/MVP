import ollama
import time
import sys

# التأكد من أن المخرجات تظهر فوراً في سجلات Hugging Face
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# --- الإعدادات الرئيسية للوكيل ---
OBJECTIVE = "Write a short, inspiring story about a small seed that grows into a giant tree."
FIRST_TASK = "Develop a character for the seed, giving it a name and a personality."

# --- تهيئة قائمة المهام ---
task_list = [FIRST_TASK]

print("=" * 30)
print("🚀 INDEPENDENT AGENT v1.0 (STABLE) 🚀")
print("=" * 30)
print(f"OBJECTIVE: {OBJECTIVE}")
print("-" * 30)

# --- حلقة التفكير والتنفيذ الرئيسية ---
while len(task_list) > 0:
    current_task = task_list.pop(0)
    print(f"🔥 EXECUTING TASK: {current_task}")

    execution_prompt = f"You are part of an AI agent. Your main objective is: '{OBJECTIVE}'. Please execute the following task: '{current_task}'"
        
    try:
        response = ollama.chat(
            model='tinylama',
            messages=[{'role': 'user', 'content': execution_prompt}],
            stream=False
        )
        execution_result = response['message']['content']
        print(f"✅ TASK RESULT: {execution_result}")
    except Exception as e:
        print(f"❌ ERROR DURING EXECUTION: {e}")
        continue

    generation_prompt = f"""
    You are a task creation AI. Your main objective is: '{OBJECTIVE}'.
    The last task was: '{current_task}'.
    The result of that task was: '{execution_result}'.
    Based on this, create a list of new tasks to continue working towards the main objective.
    Return the tasks as a Python list of strings, like ["task 1", "task 2"].
    Do not include the first task. Make the tasks short and clear.
    """

    try:
        response = ollama.chat(
            model='tinylama',
            messages=[{'role': 'user', 'content': generation_prompt}],
            stream=False
        )
        new_tasks_str = response['message']['content']
            
        try:
            start_index = new_tasks_str.find('[')
            end_index = new_tasks_str.rfind(']')
            if start_index != -1 and end_index != -1:
                new_tasks = eval(new_tasks_str[start_index:end_index+1])
                task_list.extend(new_tasks)
                print(f"📝 NEW TASKS ADDED: {new_tasks}")
            else:
                print("⚠️ Could not parse new tasks.")
        except:
            print("⚠️ Error parsing new tasks.")

    except Exception as e:
        print(f"❌ ERROR DURING TASK GENERATION: {e}")

    print("-" * 30)
    time.sleep(2) # زدنا فترة الانتظار قليلاً

print("🎉 ALL TASKS COMPLETED. OBJECTIVE ACHIEVED. 🎉")
