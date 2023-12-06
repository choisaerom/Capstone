import pandas as pd

# 함수 데이터
file_path_0 = r'd:\고려대 4학년 2학기\캡스톤 디자인\IAT feature\function\functions_label_0.csv'
file_path_1 = r'd:\고려대 4학년 2학기\캡스톤 디자인\IAT feature\function\functions_label_1.csv'

# 두 CSV 파일을 로드
data_0 = pd.read_csv(file_path_0)
data_1 = pd.read_csv(file_path_1)

#결합
combined_data = pd.concat([data_0, data_1])
combined_data.drop_duplicates(inplace=True)

functions_list = [
   "GetUserDefaultLCID", "SizeofResource", "MoveFileW", "LockResource", "LocalAlloc",
    "InitializeCriticalSection", "GetThreadLocale", "GetModuleHandleA", "GetLocaleInfoA", 
    "ExitThread", "EnumCalendarInfoA", "DeleteFileW", "CharLowerBuffA", 
    "TryEnterCriticalSection", "SysReAllocStringLen", "SysFreeString", "SysAllocStringLen", 
    "SuspendThread", "SetThreadLocale", "SetFilePointer", "ResumeThread", "ReadFile", 
    "LoadResource", "LeaveCriticalSection", "GetThreadPriority", "GetStdHandle", 
    "GetStartupInfoA", "GetProcessHeap", "GetProcAddress", "GetCurrentThreadId", 
    "FreeResource", "FreeLibrary", "FindResourceExA", "EnumResourceTypesA", 
    "EnumResourceNamesA", "EnumResourceLanguagesA", "EnterCriticalSection", 
    "DeleteCriticalSection", "CreateFileW", "CreateEventA", "CompareStringA", 
    "CloseHandle", "CharUpperBuffA", "CharLowerA", "SetThreadToken", 
    "ChildWindowFromPoint", "CharToOemW", "_wcslwr", "BuildCommDCBAndTimeoutsW",
    "GetTapeParameters", "BackupEventLogA", "WriteConsoleOutputCharacterA",
    "WriteConsoleOutputAttribute"
]

# 데이터를 파일 이름별로 그룹화하고 함수 목록을 집계
grouped_data = combined_data.groupby('file_name')['function'].apply(list).reset_index()

# 결과를 저장할 새 DataFrame을 초기화
results_df = pd.DataFrame()
results_df['file_name'] = grouped_data['file_name']

# 각 파일에 대해 제공된 함수 목록의 각 함수가 차지하는 비율을 계산
for func in functions_list:
    func_percentages = []
    for _, row in grouped_data.iterrows():
        total_functions = len(row['function'])
        func_count = row['function'].count(func)
        percentage = (func_count / total_functions * 100) if total_functions > 0 else 0
        func_percentages.append(percentage)
    results_df[func] = func_percentages

# 결과 DataFrame을 CSV 파일로 저장
output_csv_path = r'D:\고려대 4학년 2학기\캡스톤 디자인\feature set/combined_functions_percentage.csv'
results_df.to_csv(output_csv_path, index=False)


#모듈 데이터
file_names_path =r'd:\고려대 4학년 2학기\캡스톤 디자인\file_name.xlsx'
modules_path_0 = r'd:\고려대 4학년 2학기\캡스톤 디자인\IAT feature\moduel\modules_label_0.csv'
modules_path_1 = r'd:\고려대 4학년 2학기\캡스톤 디자인\IAT feature\moduel\modules_label_1.csv'

# Excel 파일 로드 (첫 번째 행을 헤더로 사용)
file_names_df = pd.read_excel(file_names_path, header=None)
file_names_df.columns = ['file_name']


modules_data_0 = pd.read_csv(modules_path_0)
modules_data_1 = pd.read_csv(modules_path_1)
combined_modules_data = pd.concat([modules_data_0, modules_data_1])
combined_modules_data.drop_duplicates(inplace=True)

# 검사할 모듈 목록
modules_list = [
    "kernel32.dll", "user32.dll", "oleaut32.dll", "ole32.dll", "SHLWAPI.DLL",
    "advapi32.dll", "SHELL32.dll", "gdi32.dll", "comctl32.dll", "MSVCRT.dll",
    "WININET.dll", "mscoree.dll", "PSAPI.DLL", "version.dll", "WS2_32.dll",
    "gdiplus.dll", "USERENV.dll", "MSVBVM60.DLL", "wsock32.dll", "WINSPOOL.DRV",
    "WTSAPI32.dll", "MSIMG32.dll", "WINMM.dll", "RPCRT4.DLL", "comdlg32.dll",
    "IPHLPAPI.DLL", "ATL.DLL", "netapi32.dll", "ntdll.dll", "MPR.DLL",
    "CRYPT32.dll", "MSVCP60.dll", "UxTheme.dll", "rtl60.bpl", "ibxpress60.bpl",
    "xmlrtl60.bpl", "Cabinet.dll", "api-ms-win-crt-utility-l1-1-0.dll", "msys-2.0.dll",
    "api-ms-win-core-console-l2-1-0.dll", "api-ms-win-core-libraryloader-l1-2-0.dll"
]

results_df = pd.DataFrame(columns=['file_name'] + modules_list)

# file_name.xlsx 파일의 파일 이름 설정
results_df['file_name'] = file_names_df['file_name']

grouped_modules_data = combined_modules_data.groupby('file_name')['module'].apply(list).reset_index()

# 각 파일에 대해 모듈 비율 계산
for index, row in results_df.iterrows():
    file_name = row['file_name']
    if file_name in grouped_modules_data['file_name'].values:
        modules = grouped_modules_data[grouped_modules_data['file_name'] == file_name].iloc[0]['module']
        total_modules = len(modules)
        for module in modules_list:
            module_count = modules.count(module)
            percentage = (module_count / total_modules * 100) if total_modules > 0 else 0
            results_df.at[index, module] = percentage
    else:
        results_df.loc[index, modules_list] = 0

# 결과를 CSV 파일로 저장
output_csv_path = r'D:\고려대 4학년 2학기\캡스톤 디자인\feature set\complete_module_percentages.csv'
results_df.to_csv(output_csv_path, index=False)