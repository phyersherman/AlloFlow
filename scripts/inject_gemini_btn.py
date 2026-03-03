import sys
import re

file_path = r'c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    target = '<label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Phonemes</label>'
    
    replacement = """<div className="flex items-center gap-2">
                                                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Phonemes</label>
                                                    <button
                                                        onClick={() => onRegenerateWord && onRegenerateWord(idx)}
                                                        disabled={regeneratingIndex === idx}
                                                        className={`text-[10px] px-2 py-0.5 rounded-full flex items-center gap-1 font-bold transition-colors ${regeneratingIndex === idx ? 'bg-slate-100 text-slate-400' : 'bg-violet-100 text-violet-600 hover:bg-violet-200'}`}
                                                        title="Re-check phonemes with Gemini"
                                                    >
                                                        {regeneratingIndex === idx ? <div className="animate-spin h-3 w-3 border-2 border-current border-t-transparent rounded-full" /> : '✨'}
                                                        Check
                                                    </button>
                                                </div>"""

    if target in content:
        # We only want to replace the first instance (there's probably only one, but just in case)
        new_content = content.replace(target, replacement, 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('SUCCESS: Replaced content in AlloFlowANTI.txt')
    else:
        print('ERROR: Target string not found.')

except Exception as e:
    print(f'ERROR: {e}')
