import ollama
import time
import sys
import json # <-- 1. استيراد مكتبة للتعامل مع ملفات الذاكرة
import os   # <-- 2. استيراد مكتبة للتحقق من وجود الملفات

# --- اسم ملف الذاكرة ---
MEMORY_FILE = "agent_memory.json"

# التأكد من أن المخرجات تظهر فوراً
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# --- دالة لحفظ الذاكرة ---
def save_memory(task_list, completed_tasks):
    memory = {
        "task_list": task_list,
        "completed_tasks": completed_tasks
    }
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

# --- دالة لتحميل الذاكرة ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return None

# --- الإعدادات الرئيسية للوكيل ---
OBJECTIVE = "Write a short, inspiring story about a small seed that grows into a giant tree."
FIRST_TASK = "Develop a character for the seed, giving it a name and a personality."

# --- تهيئة قوائم المهام ---
task_list = []
completed_tasks = []

# --- 3. محاولة تحميل الذاكرة عند البدء ---
saved_memory = load_memory()
if saved_memory:
    print("🧠 Memory found! Loading previous state...")
    task_list = saved_memory['task_list']
    completed_tasks = saved_memory['completed_tasks']
    if not task_list: # إذا كانت قائمة المهام فارغة بعد التحميل، أضف المهمة الأولى
        task_list.append(FIRST_TASK)
else:
    print("🧠 No memory found. Starting fresh.")
    task_list.append(FIRST_TASK)


print("=" * 30)
print("🚀 INDEPENDENT AGENT v4.1 (MEMORY EDITION) 🚀")
print("=" * 30)
print(f"OBJECTIVE: {OBJECTIVE}")
print("-" * 30)

# --- 4. تشغيل الخادم في الخلفية (فقط إذا لم يكن يعمل بالفعل) ---
# هذه الخطوة تتم يدوياً في الطرفية قبل تشغيل الكود

# --- حلقة التفكير والتنفيذ الرئيسية ---
while len(task_list) > 0:
    current_task = task_list.pop(0)
    print(f"🔥 EXECUTING TASK: {current_task}")

    execution_prompt = f"You are part of an AI agent. Your main objective is: '{OBJECTIVE}'. You have completed these tasks: {completed_tasks}. Please execute the following task: '{current_task}'"
    
    try:
        response = ollama.chat(
            model='tinylama:1.1b',
            messages=[{'role': 'user', 'content': execution_prompt}],
            stream=False
        )
        execution_result = response['message']['content']
        print(f"✅ TASK RESULT: {execution_result}")
        completed_tasks.append(current_task) # <-- 5. إضافة المهمة المكتملة للذاكرة
    except Exception as e:
        print(f"❌ ERROR DURING EXECUTION: {e}")
        task_list.insert(0, current_task) # أعد المهمة إلى القائمة لإعادة المحاولة
        save_memory(task_list, completed_tasks) # احفظ الحالة قبل الخروج
        continue

    generation_prompt = f"""
    You are a task creation AI. Your main objective is: '{OBJECTIVE}'.
    You have completed these tasks: {completed_tasks}.
    The last task was: '{current_task}'.
    The result of that task was: '{execution_result}'.
    Based on this, create a list of new tasks to continue working towards the main objective.
    Return the tasks as a Python list of strings, like ["task 1", "task 2"]. Do not repeat tasks that are already completed.
    """

    try:
        response = ollama.chat(
            model='tinylama:1.1b',
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

    # --- 6. حفظ الذاكرة بعد كل دورة ---
    save_memory(task_list, completed_tasks)
    print("💾 Memory saved.")
    print("-" * 30)
    time.sleep(2)

print("🎉 ALL TASKS COMPLETED. OBJECTIVE ACHIEVED. 🎉")

