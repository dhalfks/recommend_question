import pandas as pd

# Let's write the complete dataset directly and export to Excel file.

questions = []

def add_q(code, unit, content, snippet, diff, btime, op1, op2, op3, op4, correct, exp, tags):
    questions.append({
        "subject_code": code,
        "subject_unit": unit,
        "content": content,
        "code_snippet": snippet if snippet else "",
        "difficulty": diff,
        "benchmark_time": btime,
        "option_1": op1,
        "option_2": op2,
        "option_3": op3,
        "option_4": op4,
        "correct_option": correct,
        "explanation": exp,
        "tags": tags,
        "is_required": False
    })

def make_qs(code, unit, q_list):
    for q in q_list:
        add_q(code, unit, q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10])

# ================= JAVA (6 units x 10 = 60) =================
make_qs("JAVA", "기본구문(조건문, 반복문)", [
    ["다음 자바 코드의 실행 결과로 올바른 것은?", "int a = 5;\nif (a % 2 == 0) {\n    System.out.println(\"Even\");\n} else {\n    System.out.println(\"Odd\");\n}", "EASY", 45, "Even", "Odd", "null", "컴파일 에러", 2, "5 % 2는 1이므로 else 문이 실행되어 Odd가 출력됩니다.", "Java,If-Else"],
    ["다음 switch-case 문의 출력 결과는?", "int num = 2;\nswitch(num) {\n    case 1: System.out.print(\"A\");\n    case 2: System.out.print(\"B\");\n    case 3: System.out.print(\"C\"); break;\n    default: System.out.print(\"D\");\n}", "MEDIUM", 60, "B", "BC", "ABC", "BCD", 2, "case 2에 break 문이 없으므로 fall-through가 발생하여 B와 C가 출력됩니다.", "Java,Switch"],
    ["다음 for 문이 종료될 때 sum의 값은?", "int sum = 0;\nfor(int i = 1; i <= 5; i++) {\n    if(i % 2 == 0) continue;\n    sum += i;\n}", "EASY", 50, "9", "15", "6", "10", 1, "i가 짝수인 2, 4일 때는 continue로 지나치므로 홀수 1 + 3 + 5 = 9가 됩니다.", "Java,For"],
    ["do-while 문과 while 문의 가장 큰 차이점은 무엇인가?", "", "EASY", 40, "do-while 문은 최소 1회 블록을 실행한다.", "while 문은 무한 루프가 불가능하다.", "do-while 문은 조건식을 작성하지 않는다.", "차이점이 없다.", 1, "do-while 문은 본문을 실행한 후 조건식을 검사하므로 최소 1회 실행됩니다.", "Java,Loop"],
    ["다음 삼항 연산자 코드의 실행 결과는?", "int score = 85;\nchar grade = (score >= 90) ? 'A' : (score >= 80) ? 'B' : 'C';\nSystem.out.println(grade);", "EASY", 45, "A", "B", "C", "컴파일 에러", 2, "85는 90 미만, 80 이상이므로 중첩 삼항 연산자에 의해 'B'가 됩니다.", "Java,Operator"],
    ["다음 중 자바의 식별자 작성 규칙으로 올바르지 않은 것은?", "", "EASY", 40, "첫 글자로 숫자가 올 수 없다.", "특수문자는 _와 $만 허용된다.", "자바 예약어는 식별자로 사용할 수 없다.", "대소문자를 구분하지 않는다.", 4, "자바는 대소문자를 엄격히 구분합니다.", "Java,Syntax"],
    ["다음 조건식 중 변수 x가 10 이상 20 이하일 때 true가 되는 식은?", "", "EASY", 30, "10 <= x <= 20", "x >= 10 && x <= 20", "x >= 10 || x <= 20", "x >= 10 AND x <= 20", 2, "자바에서는 논리 연산자 &&를 사용해 조건식을 연결합니다.", "Java,Logic"],
    ["다음 무한 루프를 만드는 구문 중 틀린 것은?", "", "EASY", 35, "for(;;)", "while(true)", "while(1)", "do {} while(true)", 3, "자바의 while 문 조건식은 반드시 boolean 타입이어야 하므로 while(1)은 컴파일 에러입니다.", "Java,Loop"],
    ["다음 코드 실행 시 출력되는 값은?", "int x = 10;\nint y = x++;\nSystem.out.println(y + \" \" + x);", "MEDIUM", 50, "10 10", "10 11", "11 11", "11 10", 2, "후위 증가 연산자(x++)는 y에 x(10)가 대입된 후 x가 11로 증가합니다.", "Java,Operator"],
    ["다음 중 break 문과 continue 문에 대한 설명으로 올바른 것은?", "", "EASY", 40, "break는 루프의 다음 회차로 이동한다.", "continue는 가장 가까운 반복문을 완전히 탈출한다.", "break는 switch문과 반복문에서 모두 사용 가능하다.", "continue는 switch문에서 사용 가능하다.", 3, "break는 switch문과 반복문을 탈출할 때 사용되며, continue는 다음 회차로 이동합니다.", "Java,ControlFlow"]
])

make_qs("JAVA", "객체지향개념", [
    ["객체지향 프로그래밍의 4대 특징에 해당하지 않는 것은?", "", "EASY", 30, "캡슐화", "상속", "다형성", "절차성", 4, "객체지향 4대 특징은 캡슐화, 상속, 다형성, 추상화입니다.", "Java,OOP"],
    ["다음 코드의 출력으로 올바른 것은?", "class Parent { void show() { System.out.println(\"Parent\"); } }\nclass Child extends Parent { void show() { System.out.println(\"Child\"); } }\nParent p = new Child(); p.show();", "MEDIUM", 60, "Parent", "Child", "컴파일 에러", "런타임 에러", 2, "오버라이딩된 메서드는 실제 생성된 객체(Child)의 메서드가 호출됩니다.", "Java,Polymorphism"],
    ["접근 제어자의 접근 범위가 가장 넓은 것부터 좁은 순서로 바르게 나열된 것은?", "", "MEDIUM", 50, "public > protected > default > private", "public > default > protected > private", "protected > public > default > private", "public > protected > private > default", 1, "public > protected > default > private 순입니다.", "Java,AccessModifier"],
    ["추상 클래스와 인터페이스에 대한 설명으로 틀린 것은?", "", "HARD", 70, "추상 클래스는 단일 상속만 가능하다.", "인터페이스는 다중 구현이 가능하다.", "인터페이스는 인스턴스 필드를 선언할 수 있다.", "추상 클래스는 생성자를 가질 수 있다.", 3, "인터페이스의 필드는 static final 상수만 가능합니다.", "Java,Interface"],
    ["오버로딩(Overloading)의 성립 조건으로 올바른 것은?", "", "MEDIUM", 50, "메서드 이름이 같고 매개변수의 개수나 타입이 달라야 한다.", "리턴 타입만 다르면 오버로딩이 성립한다.", "접근 제어자만 다르면 성립한다.", "매개변수 이름이 달라야 한다.", 1, "오버로딩은 메서드 이름이 같고 매개변수 시그니처가 달라야 합니다.", "Java,Overloading"],
    ["static 키워드에 대한 설명으로 올바르지 않은 것은?", "", "EASY", 40, "static 멤버는 클래스 로딩 시 메모리에 할당된다.", "static 메서드 내에서는 인스턴스 변수에 직접 접근할 수 없다.", "객체 생성 없이 호출 가능하다.", "static 변수는 객체마다 독립된 값을 가진다.", 4, "static 변수는 클래스의 모든 인스턴스가 공유합니다.", "Java,Static"],
    ["자바에서 클래스 상속 및 메서드 재정의를 금지할 때 사용하는 키워드는?", "", "EASY", 30, "static", "final", "abstract", "transient", 2, "final 키워드를 사용합니다.", "Java,Final"],
    ["생성자(Constructor)에 대한 설명으로 올바른 것은?", "", "EASY", 40, "반환 타입으로 void를 지정해야 한다.", "클래스 내에 생성자가 없으면 기본 생성자가 자동 추가된다.", "생성자는 상속된다.", "new 키워드 없이 직접 호출 가능하다.", 2, "생성자가 정의되어 있지 않으면 기본 생성자가 자동 생성됩니다.", "Java,Constructor"],
    ["super() 키워드의 용도로 올바른 것은?", "", "EASY", 40, "부모 클래스의 생성자를 호출한다.", "자신 클래스의 다른 생성자를 호출한다.", "부모 클래스를 인스턴스화한다.", "정적 메서드를 호출한다.", 1, "super()는 부모 클래스 생성자를 호출합니다.", "Java,Super"],
    ["정보 은닉(Data Hiding)을 구현하기 위한 가장 적절한 방법은?", "", "EASY", 40, "필드를 public으로 선언한다.", "필드를 private으로 선언하고 Getter/Setter를 제공한다.", "필드를 static으로 선언한다.", "모든 메서드를 private으로 선언한다.", 2, "private 필드와 public Getter/Setter가 표준입니다.", "Java,Encapsulation"]
])

make_qs("JAVA", "스레드", [
    ["자바에서 스레드를 생성하는 두 가지 대표적인 방법은?", "", "EASY", 40, "Thread 클래스 상속 / Runnable 인터페이스 구현", "Object 상속 / Process 구현", "Task 클래스 상속 / Executable 구현", "Stream 상속 / Future 구현", 1, "Thread 상속과 Runnable 구현이 기본 방법입니다.", "Java,Thread"],
    ["스레드를 실행시키기 위해 호출해야 하는 메서드는?", "", "EASY", 30, "run()", "start()", "execute()", "init()", 2, "start() 메서드를 호출해야 새 스레드의 콜 스택이 생성되고 run()이 실행됩니다.", "Java,ThreadStart"],
    ["멀티스레드 환경에서 공유 자원의 동기화를 위해 사용하는 키워드는?", "", "EASY", 30, "volatile", "synchronized", "transient", "static", 2, "synchronized 키워드를 통해 임계 영역을 동기화합니다.", "Java,Synchronized"],
    ["다음 스레드의 상태 중 일시 정지(Waiting/Timed Waiting) 상태에 해당하지 않는 것은?", "", "MEDIUM", 50, "NEW", "BLOCKED", "WAITING", "TIMED_WAITING", 1, "NEW는 스레드 객체가 생성되었으나 아직 start()가 호출되지 않은 상태입니다.", "Java,ThreadState"],
    ["sleep() 메서드에 대한 설명으로 올바른 것은?", "", "EASY", 40, "Thread의 static 메서드이다.", "락(Lock)을 해제하고 대기한다.", "InterruptedException을 발생시키지 않는다.", "Object 클래스의 메서드이다.", 1, "sleep()은 Thread 클래스의 정적 메서드이며, 락을 유지한 채 일시정지합니다.", "Java,Sleep"],
    ["wait()와 notify() 메서드가 속한 클래스는?", "", "MEDIUM", 50, "Thread", "Runnable", "Object", "Process", 3, "wait(), notify(), notifyAll()은 Object 클래스에 정의되어 있습니다.", "Java,ObjectWait"],
    ["데드락(Deadlock, 교착상태)이 발생하는 4가지 필요조건에 해당하지 않는 것은?", "", "HARD", 70, "상호 배제 (Mutual Exclusion)", "점유와 대기 (Hold and Wait)", "선점 (Preemption)", "순환 대기 (Circular Wait)", 3, "비선점(No Preemption)이 조건이며, 선점이 가능하면 데드락이 발생하지 않습니다.", "Java,Deadlock"],
    ["ThreadLocal 클래스의 주된 용도는?", "", "HARD", 65, "스레드 간 변수 공유", "스레드 단위의 독립적인 변수 저장소 제공", "스레드 개수 제한", "스레드 우선순위 변경", 2, "ThreadLocal은 각 스레드별 독립적인 변수 공간을 제공합니다.", "Java,ThreadLocal"],
    ["java.util.concurrent 패키지의 ExecutorService 종료 시 사용하는 메서드는?", "", "MEDIUM", 50, "stop()", "shutdown()", "destroy()", "finish()", 2, "ExecutorService는 shutdown() 또는 shutdownNow()를 사용해 종료합니다.", "Java,ExecutorService"],
    ["volatile 키워드의 주요 역할은?", "", "HARD", 70, "원자성(Atomicity) 보장", "변수의 가시성(Visibility) 보장 (메인 메모리 직접 읽기/쓰기)", "스레드 락 생성", "객체 직렬화 제외", 2, "volatile은 CPU 캐시가 아닌 메인 메모리 직접 참조를 통해 변수의 가시성을 보장합니다.", "Java,Volatile"]
])

make_qs("JAVA", "Collection Framework", [
    ["Collection 인터페이스를 상속받지 않는 Map 계열 컬렉션은?", "", "EASY", 30, "ArrayList", "HashSet", "HashMap", "LinkedList", 3, "Map은 Collection 인터페이스를 상속받지 않는 별도의 구조입니다.", "Java,Collection"],
    ["다음 중 순서를 유지하고 중복을 허용하는 컬렉션 인터페이스는?", "", "EASY", 30, "Set", "List", "Map", "Queue", 2, "List 인터페이스는 순서 유지 및 중복을 허용합니다.", "Java,List"],
    ["List 구현체 중 요소의 삽입/삭제가 빈번할 때 가장 유리한 구조는?", "", "EASY", 40, "ArrayList", "LinkedList", "Vector", "ArrayDeque", 2, "LinkedList는 노드 포인터만 변경하므로 중간 삽입/삭제 성능이 우수합니다.", "Java,LinkedList"],
    ["Set 구현체 중 요소를 자동으로 정렬하여 저장하는 클래스는?", "", "MEDIUM", 50, "HashSet", "LinkedHashSet", "TreeSet", "CopyOnWriteArraySet", 3, "TreeSet은 이진 탐색 트리를 기반으로 요소를 오름차순 정렬 저장합니다.", "Java,TreeSet"],
    ["HashMap에서 Key 객체의 중복 판단 시 사용하는 두 메서드는?", "", "MEDIUM", 60, "toString() & equals()", "hashCode() & equals()", "compareTo() & equals()", "clone() & hashCode()", 2, "HashMap은 hashCode() 비교 후 동등할 경우 equals()로 최종 검증합니다.", "Java,HashMap"],
    ["List의 요소를 정렬할 때 사용하는 Collections 클래스의 메서드는?", "", "EASY", 30, "Collections.sort()", "Collections.order()", "Collections.arrange()", "Collections.group()", 1, "Collections.sort()를 사용하여 정렬합니다.", "Java,Collections"],
    ["Stack 클래스는 LIFO 구조입니다. FIFO 구조를 지원하는 컬렉션 인터페이스는?", "", "EASY", 40, "Set", "Queue", "Map", "List", 2, "Queue 인터페이스가 FIFO(First In First Out) 구조입니다.", "Java,Queue"],
    ["Iterator 인터페이스의 주요 메서드가 아닌 것은?", "", "EASY", 40, "hasNext()", "next()", "remove()", "add()", 4, "Iterator에는 add() 메서드가 없으며 순회 및 삭제만 제공합니다.", "Java,Iterator"],
    ["멀티스레드 환경에서 안전한(Thread-safe) Map 구현체는?", "", "MEDIUM", 50, "HashMap", "ConcurrentHashMap", "TreeMap", "LinkedHashMap", 2, "ConcurrentHashMap은 세그먼트/버킷 단위 락을 사용하여 멀티스레드 안전을 제공합니다.", "Java,ConcurrentHashMap"],
    ["ArrayList의 기본 초기 용량(Capacity)은 얼마인가?", "", "EASY", 35, "5", "10", "16", "20", 2, "ArrayList의 기본 초기 용량은 10입니다.", "Java,ArrayList"]
])

make_qs("JAVA", "자료구조", [
    ["배열(Array)의 특징으로 올바르지 않은 것은?", "", "EASY", 35, "크기가 고정되어 있다.", "인덱스를 통한 접근 속도는 O(1)이다.", "동적으로 크기를 늘릴 수 있다.", "연속된 메모리 공간에 저장된다.", 3, "자바의 기본 배열은 생성 후 크기 변경이 불가능합니다.", "Java,Array"],
    ["스택(Stack) 자료구조의 동작 방식은?", "", "EASY", 30, "FIFO", "LIFO", "FILO 및 LIFO", "Random", 3, "스택은 LIFO (Last In First Out) 구조입니다.", "Java,Stack"],
    ["큐(Queue)에서 데이터를 넣는 연산과 빼는 연산의 이름은?", "", "EASY", 40, "push / pop", "offer(enqueue) / poll(dequeue)", "add / remove", "insert / delete", 2, "큐에서는 offer/poll 또는 enqueue/dequeue를 사용합니다.", "Java,QueueOps"],
    ["해시 테이블(Hash Table)에서 서로 다른 Key가 동일한 해시 값을 가질 때 발생하는 현상은?", "", "EASY", 40, "해시 충돌 (Hash Collision)", "해시 오버플로우", "null 포인터 에러", "데드락", 1, "이를 해시 충돌이라고 부릅니다.", "Java,Hash"],
    ["이진 탐색 트리(BST)에서 최악의 경우(한쪽으로 치우친 트리) 탐색 시간 복잡도는?", "", "HARD", 65, "O(1)", "O(log N)", "O(N)", "O(N^2)", 3, "편향 트리가 될 경우 탐색 시간 복잡도는 O(N)으로 저하됩니다.", "Java,BST"],
    ["연결 리스트(LinkedList)의 단점으로 올바른 것은?", "", "MEDIUM", 50, "데이터 삽입이 어렵다.", "특정 인덱스 접근 시 O(N)의 시간이 소요된다.", "크기가 고정되어 있다.", "메모리를 재사용할 수 없다.", 2, "임의 접근(Random Access)이 불가하여 N번째 노드 접근 시 차례대로 순회해야 합니다.", "Java,LinkedListDs"],
    ["그래프(Graph) 탐색 알고리즘 중 큐(Queue)를 활용하는 방식은?", "", "MEDIUM", 50, "DFS (깊이 우선 탐색)", "BFS (너비 우선 탐색)", "Dijkstra", "Binary Search", 2, "BFS는 큐를 활용하여 인접한 노드를 먼저 방문합니다.", "Java,BFS"],
    ["최소 힙(Min Heap)에서 루트 노드가 갖는 값은?", "", "MEDIUM", 45, "트리 내의 최댓값", "트리 내의 최솟값", "중간값", "랜덤값", 2, "최소 힙의 루트 노드는 항상 전체 요소 중 최솟값을 유지합니다.", "Java,Heap"],
    ["다음 중 정렬 알고리즘의 평균 시간 복잡도가 O(N log N)인 것은?", "", "MEDIUM", 50, "버블 정렬", "선택 정렬", "퀵 정렬 (Quick Sort)", "삽입 정렬", 3, "퀵 정렬, 병합 정렬, 힙 정렬의 평균 시간 복잡도는 O(N log N)입니다.", "Java,Sorting"],
    ["원형 큐(Circular Queue)를 사용하는 주된 이유는?", "", "HARD", 60, "메모리 무제한 확장", "선형 큐의 메모리 낭비(공간 재사용 불가) 해결", "자동 정렬 기능 제공", "LIFO 구조 구현", 2, "선형 큐에서 front가 이동하면서 생기는 앞쪽의 빈 공간을 재사용하기 위해 원형 큐를 사용합니다.", "Java,CircularQueue"]
])

make_qs("JAVA", "람다/스트림", [
    ["자바 8에서 도입된 람다식(Lambda Expression)의 기본 문법 형태는?", "", "EASY", 30, "(매개변수) -> { 바디 }", "(매개변수) => { 바디 }", "function(매개변수) {}", "lambda(매개변수) : 바디", 1, "자바 람다식은 (매개변수) -> { 바디 } 문법을 사용합니다.", "Java,Lambda"],
    ["함수형 인터페이스(Functional Interface)의 정의는?", "", "EASY", 30, "메서드가 하나도 없는 인터페이스", "추상 메서드가 단 하나만 존재하는 인터페이스", "모든 메서드가 default 메서드인 인터페이스", "static 메서드만 가진 인터페이스", 2, "추상 메서드가 오직 1개인 인터페이스를 의미합니다.", "Java,FunctionalInterface"],
    ["함수형 인터페이스를 나타내기 위해 붙이는 어노테이션은?", "", "EASY", 30, "@FunctionalInterface", "@Lambda", "@Stream", "@Function", 1, "@FunctionalInterface 어노테이션을 사용합니다.", "Java,Annotation"],
    ["다음 Stream 연산 중 중간 연산(Intermediate Operation)에 해당하는 것은?", "", "MEDIUM", 50, "forEach()", "collect()", "filter()", "count()", 3, "filter(), map(), sorted() 등은 Stream을 반환하는 중간 연산입니다.", "Java,StreamFilter"],
    ["다음 Stream 연산 중 최종 연산(Terminal Operation)에 해당하는 것은?", "", "MEDIUM", 50, "map()", "distinct()", "collect()", "limit()", 3, "collect(), forEach(), count() 등은 결과를 도출하는 최종 연산입니다.", "Java,StreamCollect"],
    ["다음 코드의 실행 결과 출력되는 값은?", "List<Integer> list = List.of(1, 2, 3, 4, 5);\nint sum = list.stream().filter(n -> n % 2 == 0).mapToInt(n -> n).sum();\nSystem.out.println(sum);", "MEDIUM", 60, "6", "15", "9", "3", 1, "짝수인 2, 4만 필터링되어 합산되면 6이 됩니다.", "Java,StreamExam"],
    ["Optional 클래스의 용도로 올바른 것은?", "", "EASY", 40, "NullPointerException을 방지하고 null 가능성을 명시적으로 표현", "성능 향상", "멀티스레드 동기화", "데이터 암호화", 1, "NullPointerException 예방 및 세련된 null 처리를 위해 사용합니다.", "Java,Optional"],
    ["메서드 참조(Method Reference)의 올바른 표현식은?", "", "EASY", 35, "String::valueOf", "String->valueOf", "String.valueOf()", "String@valueOf", 1, "클래스명::메서드명 형태로 작성합니다.", "Java,MethodReference"],
    ["자바의 표준 함수형 인터페이스 중 매개변수가 있고 반환값이 boolean인 것은?", "", "HARD", 60, "Consumer<T>", "Supplier<T>", "Predicate<T>", "Function<T, R>", 3, "Predicate<T>는 T를 받아 boolean을 반환하는 test() 메서드를 가집니다.", "Java,Predicate"],
    ["Stream의 map()과 flatMap()의 차이점은?", "", "HARD", 70, "map은 1:1 변환, flatMap은 중첩 구조를 평평하게(1:N) 변환", "map은 최종연산, flatMap은 중간연산", "차이가 없다.", "map은 정수형만 가능", 1, "flatMap은 요소를 스트림으로 변환 후 하나로 합쳐 평평하게 만듭니다.", "Java,FlatMap"]
])

# ================= SQL (6 units x 10 = 60) =================
make_qs("SQL", "기본 SQL 개념", [
    ["관계형 데이터베이스(RDBMS)의 특징이 아닌 것은?", "", "EASY", 30, "데이터를 테이블(Table) 형태로 관리한다.", "SQL 언어를 사용하여 제어한다.", "데이터 간의 관계(Relationship)를 정의한다.", "키-값(Key-Value) 쌍으로만 저장된다.", 4, "Key-Value 방식은 NoSQL의 대표적인 특징입니다.", "SQL,RDBMS"],
    ["다음 중 데이터의 중복을 제거하고 조회할 때 사용하는 SQL 키워드는?", "", "EASY", 30, "UNIQUE", "DISTINCT", "GROUP BY", "ORDER BY", 2, "DISTINCT 키워드는 조회 결과에서 중복행을 제거합니다.", "SQL,Distinct"],
    ["NULL 값과의 연산 결과로 올바른 것은?", "", "EASY", 35, "0", "NULL", "공백", "오류 발생", 2, "NULL과의 산술 연산 결과는 항상 NULL입니다.", "SQL,Null"],
    ["NULL 값을 다른 값으로 대체할 수 있는 ANSI SQL 표준 함수는?", "", "EASY", 40, "NVL", "IFNULL", "COALESCE", "ISNULL", 3, "COALESCE 함수는 ANSI SQL 표준 인자 중 첫 번째 non-null 값을 반환합니다.", "SQL,Coalesce"],
    ["ORDER BY 절에서 내림차순 정렬을 지정하는 키워드는?", "", "EASY", 30, "ASC", "DESC", "DOWN", "TOP", 2, "내림차순 정렬에는 DESC 키워드를 사용합니다.", "SQL,OrderBy"],
    ["WHERE 절에서 특정 패턴(와일드카드 문자 %, _)을 검색할 때 사용하는 연산자는?", "", "EASY", 30, "LIKE", "MATCH", "IN", "BETWEEN", 1, "LIKE 연산자를 패턴 매칭에 사용합니다.", "SQL,Like"],
    ["HAVING 절에 대한 설명으로 올바른 것은?", "", "MEDIUM", 50, "WHERE 절 이전에 실행된다.", "그룹화된 결과(GROUP BY)에 대한 조건 필터링에 사용된다.", "개별 행에 대한 조건을 설정한다.", "ORDER BY 절 다음에 배치된다.", 2, "HAVING 절은 GROUP BY 결과 집계에 대한 조건을 지정합니다.", "SQL,Having"],
    ["두 테이블을 조인할 때 교집합 영역(공통된 데이터만)을 반환하는 조인 방식은?", "", "EASY", 35, "INNER JOIN", "LEFT OUTER JOIN", "RIGHT OUTER JOIN", "FULL OUTER JOIN", 1, "INNER JOIN은 공통 조건에 일치하는 데이터만 반환합니다.", "SQL,Join"],
    ["기본키(Primary Key)의 두 가지 필수 조건은?", "", "EASY", 35, "NOT NULL & UNIQUE", "NULL 허용 & UNIQUE", "FOREIGN KEY & NOT NULL", "CHECK & DEFAULT", 1, "기본키는 고유성(UNIQUE)과 비어있지 않음(NOT NULL)을 만족해야 합니다.", "SQL,PrimaryKey"],
    ["서브쿼리(Subquery) 중 메인쿼리의 컬럼을 참조하여 실행되는 서브쿼리는?", "", "HARD", 65, "스칼라 서브쿼리", "상관 서브쿼리 (Correlated Subquery)", "인라인 뷰", "중첩 서브쿼리", 2, "상관 서브쿼리는 메인쿼리의 행 데이터를 참조하여 매 행마다 실행되는 서브쿼리입니다.", "SQL,Subquery"]
])

make_qs("SQL", "DDL", [
    ["다음 중 DDL(Data Definition Language) 명령어에 해당하지 않는 것은?", "", "EASY", 30, "CREATE", "ALTER", "DROP", "INSERT", 4, "INSERT는 DML(데이터 조작어)에 해당합니다.", "SQL,DDL"],
    ["테이블의 구조(컬럼 추가, 변경 등)를 수정할 때 사용하는 DDL 명령어는?", "", "EASY", 30, "MODIFY", "UPDATE", "ALTER", "CHANGE", 3, "ALTER TABLE 명령어로 테이블 구조를 변경합니다.", "SQL,Alter"],
    ["DROP TABLE과 TRUNCATE TABLE의 차이점으로 올바른 것은?", "", "MEDIUM", 50, "DROP은 테이블 구조까지 삭제하고, TRUNCATE는 데이터만 전체 삭제한다.", "TRUNCATE는 롤백이 불가능하나 DROP은 롤백된다.", "DROP은 데이터만 삭제한다.", "차이점이 없다.", 1, "DROP은 테이블 객체 자체를 삭제하고, TRUNCATE는 구조는 남기고 전체 행을 빠르게 삭제합니다.", "SQL,Truncate"],
    ["테이블 생성 시 컬럼의 값이 비어있지 않도록 강제하는 제약조건은?", "", "EASY", 30, "UNIQUE", "NOT NULL", "CHECK", "DEFAULT", 2, "NOT NULL 제약조건입니다.", "SQL,NotNull"],
    ["외래키(Foreign Key) 제약조건의 역할은?", "", "EASY", 40, "테이블 내의 유일성을 보장한다.", "참조 무결성(Referential Integrity)을 유지한다.", "자동 인덱스를 제거한다.", "트랜잭션을 자동으로 종료한다.", 2, "외래키는 두 테이블 간의 참조 무결성을 유지합니다.", "SQL,ForeignKey"],
    ["기존 테이블의 특정 컬럼에 인덱스(Index)를 생성하는 DDL 구문은?", "", "EASY", 40, "CREATE INDEX", "ADD INDEX", "ALTER INDEX", "MAKE INDEX", 1, "CREATE INDEX 인덱스명 ON 테이블명(컬럼명); 구문을 사용합니다.", "SQL,CreateIndex"],
    ["데이터베이스 내에 존재하는 뷰(View)를 삭제하는 명령어는?", "", "EASY", 35, "DELETE VIEW", "DROP VIEW", "REMOVE VIEW", "TRUNCATE VIEW", 2, "DROP VIEW 뷰명; 구문을 사용합니다.", "SQL,DropView"],
    ["CASCADE 옵션의 용도로 올바른 것은?", "", "MEDIUM", 50, "참조하는 상위 테이블 삭제 시 하위 데이터도 함께 삭제한다.", "데이터 삭제를 금지한다.", "임시 테이블을 생성한다.", "제약조건을 비활성화한다.", 1, "ON DELETE CASCADE는 부모 데이터 삭제 시 자식 데이터도 연쇄 삭제합니다.", "SQL,Cascade"],
    ["새로운 테이블을 만드는 DDL 명령어는?", "", "EASY", 25, "CREATE TABLE", "MAKE TABLE", "BUILD TABLE", "NEW TABLE", 1, "CREATE TABLE 구문을 사용합니다.", "SQL,CreateTable"],
    ["RENAME 명령어의 주된 목적은?", "", "EASY", 30, "데이터베이스 객체(테이블 등)의 이름을 변경한다.", "컬럼 값들을 변경한다.", "테이블을 복사한다.", "데이터 타입을 변환한다.", 1, "테이블이나 객체의 이름을 변경합니다.", "SQL,Rename"]
])

make_qs("SQL", "DML", [
    ["다음 중 DML(Data Manipulation Language) 명령어로만 묶인 것은?", "", "EASY", 30, "SELECT, INSERT, UPDATE, DELETE", "CREATE, ALTER, DROP, TRUNCATE", "GRANT, REVOKE", "COMMIT, ROLLBACK", 1, "DML은 데이터 조작어로 SELECT, INSERT, UPDATE, DELETE입니다.", "SQL,DML"],
    ["테이블에 새로운 행을 삽입하는 SQL 구문은?", "", "EASY", 30, "ADD INTO", "INSERT INTO", "PUT INTO", "APPEND INTO", 2, "INSERT INTO 테이블명 VALUES (...) 구문을 사용합니다.", "SQL,Insert"],
    ["기존 데이터를 수정할 때 사용하는 SQL 구문은?", "", "EASY", 30, "CHANGE", "UPDATE", "MODIFY", "REPLACE", 2, "UPDATE 테이블명 SET 컬럼=값 WHERE 조건; 구문을 사용합니다.", "SQL,Update"],
    ["UPDATE 문에서 WHERE 절을 생략할 경우 발생하는 현상은?", "", "EASY", 35, "오류가 발생한다.", "테이블의 모든 행 데이터가 변경된다.", "첫 번째 행만 변경된다.", "아무 일도 일어나지 않는다.", 2, "WHERE 절이 없으면 테이블 전체 행이 수정됩니다.", "SQL,UpdateWarning"],
    ["테이블에서 조건에 맞는 특정 행을 삭제하는 구문은?", "", "EASY", 30, "REMOVE FROM", "DELETE FROM", "DROP FROM", "CLEAR FROM", 2, "DELETE FROM 테이블명 WHERE 조건; 구문을 사용합니다.", "SQL,Delete"],
    ["서브쿼리를 활용하여 조건에 따라 INSERT, UPDATE, DELETE를 한 번에 수행하는 구문은?", "", "HARD", 65, "UPSERT", "MERGE", "JOIN UPDATE", "CROSS DML", 2, "MERGE INTO 구문을 통해 조건부 저장/수정을 한 번에 처리합니다.", "SQL,Merge"],
    ["다음 중 여러 행의 그룹별 통계값(합계, 평균 등)을 구할 때 사용하는 함수가 아닌 것은?", "", "EASY", 40, "SUM()", "AVG()", "COUNT()", "LENGTH()", 4, "LENGTH()는 단일 행 문자열 길이 반환 함수입니다.", "SQL,GroupFunction"],
    ["WHERE 절과 HAVING 절의 차이점으로 맞는 것은?", "", "MEDIUM", 50, "WHERE는 집계함수 사용 불가, HAVING은 집계함수 조건에 사용", "WHERE는 GROUP BY 이후 동작", "HAVING은 개별 행 필터링", "차이가 없다.", 1, "WHERE 절에서는 SUM(), AVG() 같은 집계함수를 직접 조건으로 쓸 수 없고 HAVING을 써야 합니다.", "SQL,WhereVsHaving"],
    ["INSERT 문 작성 시 컬럼명을 생략할 경우 따라야 하는 규칙은?", "", "MEDIUM", 45, "모든 컬럼의 값을 테이블 정의 순서대로 전부 입력해야 한다.", "원하는 컬럼만 선택해서 넣을 수 있다.", "자동으로 NULL이 들어간다.", "컴파일 오류가 발생한다.", 1, "컬럼 리스트를 생략하면 전체 컬럼에 대해 정의된 순서대로 값을 전달해야 합니다.", "SQL,InsertRule"],
    ["SELECT 문에서 결과 데이터의 출력 개수를 제한할 때 사용하는 구문(MySQL/PostgreSQL 기준)은?", "", "EASY", 35, "LIMIT", "TOP", "ROWNUM", "STOP", 1, "MySQL과 PostgreSQL에서는 LIMIT 구문을 사용합니다.", "SQL,Limit"]
])

make_qs("SQL", "DCL", [
    ["DCL(Data Control Language)의 주요 목적은?", "", "EASY", 30, "데이터베이스 객체 생성", "데이터 조회 및 수정", "사용자 권한 부여 및 회수", "트랜잭션 확정", 3, "DCL은 데이터베이스 접근 권한을 제어합니다.", "SQL,DCL"],
    ["사용자에게 특정 권한을 부여할 때 사용하는 DCL 명령어는?", "", "EASY", 30, "GIVE", "GRANT", "ALLOW", "PERMIT", 2, "GRANT 권한 ON 객체 TO 사용자; 구문을 사용합니다.", "SQL,Grant"],
    ["사용자에게 부여했던 권한을 회수할 때 사용하는 DCL 명령어는?", "", "EASY", 30, "REVOKE", "REMOVE", "DENY", "CANCEL", 1, "REVOKE 권한 ON 객체 FROM 사용자; 구문을 사용합니다.", "SQL,Revoke"],
    ["GRANT 문에서 WITH GRANT OPTION의 의미는?", "", "HARD", 60, "부여받은 권한을 다른 사용자에게 다시 부여할 수 있는 권한을 가진다.", "모든 최고 관리자 권한을 받는다.", "권한이 즉시 취소된다.", "읽기 전용 권한만 허용한다.", 1, "권한 재부여 권한까지 함께 부여합니다.", "SQL,GrantOption"],
    ["다음 중 DCL 명령어 세트로만 이루어진 것은?", "", "EASY", 35, "GRANT, REVOKE", "COMMIT, ROLLBACK", "CREATE, DROP", "INSERT, DELETE", 1, "GRANT와 REVOKE가 DCL입니다.", "SQL,DclSet"],
    ["데이터베이스 사용자(User)를 생성하는 명령어는?", "", "EASY", 35, "CREATE USER", "ADD USER", "MAKE USER", "NEW USER", 1, "CREATE USER 구문을 사용합니다.", "SQL,CreateUser"],
    ["특정 사용자에게 부여된 권한들을 묶어서 관리하는 역할을 하는 객체는?", "", "MEDIUM", 50, "ROLE", "GROUP", "CLUSTER", "SCHEMA", 1, "ROLE(롤)을 생성하여 권한을 그룹 단위로 관리합니다.", "SQL,Role"],
    ["REVOKE CASCADE 명령의 실행 결과는?", "", "HARD", 65, "해당 사용자의 권한과, 그 사용자가 다른 이에게 부여한 권한까지 연쇄 회수된다.", "오류가 발생하여 취소된다.", "해당 사용자의 데이터가 삭제된다.", "모든 사용자의 권한이 회수된다.", 1, "연쇄적으로 재부여된 권한까지 회수됩니다.", "SQL,RevokeCascade"],
    ["DCL과 TCL을 구분할 때, COMMIT과 ROLLBACK은 무슨 언어에 속하는가?", "", "EASY", 40, "DCL", "TCL (Transaction Control Language)", "DDL", "DML", 2, "COMMIT과 ROLLBACK은 TCL(트랜잭션 제어어)입니다.", "SQL,TCL"],
    ["데이터베이스 보안 관리 차원에서 최소 권한의 원칙(Principle of Least Privilege)이란?", "", "MEDIUM", 45, "사용자에게 업무 수행에 필요한 최소한의 권한만 부여하는 것", "모든 사용자에게 관리자 권한 부여", "권한을 전혀 부여하지 않는 것", "DCL 사용 금지", 1, "보안 사고 예방을 위해 최소한의 권한만 제공합니다.", "SQL,Security"]
])

make_qs("SQL", "트랜젝션", [
    ["트랜잭션의 4가지 주요 특성(ACID)에 해당하지 않는 것은?", "", "EASY", 30, "원자성 (Atomicity)", "일관성 (Consistency)", "격리성 (Isolation)", "가용성 (Availability)", 4, "ACID는 Atomicity, Consistency, Isolation, Durability(영속성)입니다.", "SQL,ACID"],
    ["트랜잭션 작업이 성공적으로 완료되어 변경 사항을 DB에 최종 반영하는 명령어는?", "", "EASY", 30, "COMMIT", "ROLLBACK", "SAVEPOINT", "CONFIRM", 1, "COMMIT 구문으로 데이터를 영구 저장합니다.", "SQL,Commit"],
    ["트랜잭션 실행 중 오류가 발생하여 작업 전 상태로 되돌리는 명령어는?", "", "EASY", 30, "COMMIT", "ROLLBACK", "SAVEPOINT", "CANCEL", 2, "ROLLBACK 구문으로 트랜잭션을 취소하고 이전 상태로 복구합니다.", "SQL,Rollback"],
    ["트랜잭션 내에서 중간 되돌리기 지점을 지정할 때 사용하는 구문은?", "", "EASY", 40, "CHECKPOINT", "SAVEPOINT", "MARK", "BREAKPOINT", 2, "SAVEPOINT 지점명; 구문을 사용합니다.", "SQL,Savepoint"],
    ["트랜잭션의 격리 수준(Isolation Level) 중 가장 높은 격리성을 제공하나 성능이 가장 낮아지는 단계는?", "", "HARD", 70, "READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE", 4, "SERIALIZABLE 단계가 가장 높은 격리성과 안전성을 제공합니다.", "SQL,IsolationLevel"],
    ["다른 트랜잭션이 커밋하지 않은 미확정 데이터를 읽어오는 현상은?", "", "HARD", 65, "Dirty Read", "Non-Repeatable Read", "Phantom Read", "Lost Update", 1, "이를 Dirty Read 현상이라고 합니다.", "SQL,DirtyRead"],
    ["트랜잭션의 원자성(Atomicity)에 대한 가장 적절한 설명은?", "", "MEDIUM", 50, "트랜잭션 내의 모든 연산은 전체가 수행되거나 전체가 취소되어야 한다 (All or Nothing).", "트랜잭션은 항상 일관된 상태를 유지한다.", "트랜잭션끼리 서로 간섭할 수 없다.", "결과는 영구 저장된다.", 1, "원자성은 All or Nothing 특성을 의미합니다.", "SQL,Atomicity"],
    ["트랜잭션 영속성(Durability)을 보장하기 위해 데이터베이스가 사용하는 기능은?", "", "HARD", 65, "트랜잭션 로그 (Redo/Undo Log)", "메인 메모리 락", "인덱스 파일", "뷰(View)", 1, "Redo/Undo 로그를 통해 시스템 장애 발생 시 복구하여 영속성을 유지합니다.", "SQL,Durability"],
    ["오라클/PostgreSQL 등에서 DDL(CREATE 등) 수행 시 트랜잭션의 동작 방식은?", "", "MEDIUM", 55, "자동 커밋(Auto Commit)이 발생한다.", "롤백된다.", "트랜잭션이 중단된다.", "아무 일도 일어나지 않는다.", 1, "대부분의 RDBMS에서 DDL 실행 시 묵시적 커밋(Auto Commit)이 실행됩니다.", "SQL,AutoCommit"],
    ["동시성 제어(Concurrency Control)를 위해 데이터에 잠금을 거는 기법은?", "", "MEDIUM", 50, "Locking", "Hashing", "Indexing", "Partitioning", 1, "로킹(Locking) 기법을 통해 동시 접근 시 일관성을 보호합니다.", "SQL,Locking"]
])

make_qs("SQL", "프로시저/트리거", [
    ["저장 프로시저(Stored Procedure)의 장점이 아닌 것은?", "", "EASY", 40, "네트워크 트래픽 감소", "모듈화 및 재사용 가능", "보안성 향상", "데이터베이스 독립성 확보", 4, "저장 프로시저는 특정 DBMS 전용 언어(PL/SQL 등)로 작성되므로 DB 독립성이 떨어집니다.", "SQL,Procedure"],
    ["특정 테이블에 DML(INSERT, UPDATE, DELETE) 이벤트가 발생할 때 자동으로 실행되는 프로그램 객체는?", "", "EASY", 35, "트리거 (Trigger)", "프로시저 (Procedure)", "사용자 정의 함수 (User Function)", "뷰 (View)", 1, "트리거(Trigger)는 특정 데이터 이벤트에 반응하여 자동 실행됩니다.", "SQL,Trigger"],
    ["트리거 내에서 변경 전 값과 변경 후 값을 참조할 때 사용하는 의사 테이블(Pseudo Table)은?", "", "HARD", 65, "OLD & NEW", "BEFORE & AFTER", "PREV & NEXT", "SRC & DEST", 1, "트리거 내부에서는 :OLD(수정 전)와 :NEW(수정 후)를 통해 데이터에 접근합니다.", "SQL,OldNew"],
    ["저장 프로시저와 사용자 정의 함수(Function)의 결정적인 차이점은?", "", "MEDIUM", 55, "함수는 반드시 반환값(RETURN)이 존재하고 SQL 문 내부에서 사용 가능하다.", "프로시저만 매개변수를 가질 수 있다.", "함수는 DML을 자유롭게 실행할 수 있다.", "차이가 없다.", 1, "함수는 단일 값을 반환하여 SELECT절 등 SQL 문장에 직접 활용될 수 있습니다.", "SQL,FunctionVsProc"],
    ["트리거 사용 시 주의해야 할 사항은?", "", "HARD", 65, "무분별한 트리거 사용은 시스템 성능 저하 및 디버깅을 어렵게 만든다.", "트리거는 1개만 생성 가능하다.", "트리거는 파라미터를 입력받을 수 있다.", "트리거는 수동으로만 실행된다.", 1, "트리거는 연쇄 반응으로 인한 디버깅 복잡성과 성능 저하를 일으킬 수 있습니다.", "SQL,TriggerCaution"],
    ["PL/SQL 프로시저에서 예외 처리를 담당하는 블록 키워드는?", "", "EASY", 40, "EXCEPTION", "CATCH", "ERROR", "THROW", 1, "EXCEPTION 블록에서 예외를 처리합니다.", "SQL,Exception"],
    ["프로시저 정의 시 입출력 매개변수 타입을 지정할 때 쓰는 키워드가 아닌 것은?", "", "MEDIUM", 50, "IN", "OUT", "INOUT", "BOUND", 4, "프로시저 파라미터 모드는 IN, OUT, INOUT이 있습니다.", "SQL,ProcedureParam"],
    ["행 단위로 트리거가 실행되도록 지정하는 트리거 구문 옵션은?", "", "MEDIUM", 50, "FOR EACH ROW", "FOR EACH TABLE", "EVERY STATEMENT", "PER ROW", 1, "FOR EACH ROW 구문을 통해 행 단위 트리거(Row Trigger)를 설정합니다.", "SQL,ForEachRow"],
    ["트리거가 실행되는 시점을 지정하는 키워드 2가지는?", "", "EASY", 40, "BEFORE / AFTER", "START / END", "FIRST / LAST", "CREATE / DROP", 1, "이벤트 발생 전(BEFORE) 또는 후(AFTER) 시점을 지정합니다.", "SQL,TriggerTiming"],
    ["PL/SQL의 기본 블록 구조 순서로 올바른 것은?", "", "MEDIUM", 55, "DECLARE -> BEGIN -> EXCEPTION -> END", "BEGIN -> DECLARE -> END", "START -> PROCESS -> END", "DECLARE -> EXCEPTION -> END", 1, "선언부(DECLARE) -> 실행부(BEGIN) -> 예외처리부(EXCEPTION) -> 종료(END) 순입니다.", "SQL,PlSqlStructure"]
])

# ================= JS (5 units x 10 = 50) =================
make_qs("JS", "변수", [
    ["JavaScript에서 블록 스코프(Block Scope)를 가지는 변수 선언 키워드 2가지는?", "", "EASY", 30, "let, const", "var, let", "var, const", "global, local", 1, "let과 const는 블록 스코프를 지원하며 var는 함수 스코프입니다.", "JS,Variable"],
    ["const 키워드로 선언된 객체의 속성(Property)을 변경할 때 발생하는 현상은?", "", "MEDIUM", 50, "정상적으로 속성이 변경된다.", "TypeError 오류가 발생한다.", "SyntaxError 오류가 발생한다.", "속성이 무시된다.", 1, "const는 재할당이 금지되지만 참조 객체의 내부 프로퍼티 수정은 가능합니다.", "JS,ConstObject"],
    ["변수가 선언되기 전에 참조할 때 발생하는 자바스크립트 고유의 동작 메커니즘은?", "", "EASY", 40, "호이스팅 (Hoisting)", "클로저 (Closure)", "프로토타입 (Prototype)", "이벤트 루프", 1, "선언부가 스코프 상단으로 끌어올려지는 현상을 호이스팅이라고 합니다.", "JS,Hoisting"],
    ["다음 중 자바스크립트의 원시 타입(Primitive Type)이 아닌 것은?", "", "EASY", 30, "number", "string", "boolean", "object", 4, "object는 참조 타입(Reference Type)에 속합니다.", "JS,Primitive"],
    ["Symbol 데이터 타입의 주된 용도는?", "", "HARD", 60, "유일하고 변경 불가능한 고유한 객체 프로퍼티 키 생성", "문자열 결합", "빅인트 연산", "메모리 해제", 1, "Symbol은 충돌 없는 고유한 키 값을 만들 때 사용됩니다.", "JS,Symbol"],
    ["var 키워드로 선언된 변수의 기본 초기화 값은?", "", "EASY", 30, "null", "undefined", "0", "false", 2, "var 변수는 호이스팅 시 undefined로 초기화됩니다.", "JS,VarUndefined"],
    ["다음 중 typeof null 의 실행 결과로 출력되는 것은?", "", "MEDIUM", 45, "\"null\"", "\"undefined\"", "\"object\"", "\"number\"", 3, "자바스크립트의 초기 설계 오류로 typeof null은 \"object\"를 반환합니다.", "JS,TypeOfNull"],
    ["Temporal Dead Zone (TDZ)의 영향을 받는 변수 선언 키워드는?", "", "HARD", 65, "var", "let, const", "function", "import", 2, "let과 const는 선언 이전에 접근 시 TDZ에 의해 ReferenceError가 발생합니다.", "JS,TDZ"],
    ["동등 연산자(==)와 엄격 동등 연산자(===)의 차이점은?", "", "EASY", 30, "===는 값과 데이터 타입까지 비교한다.", "==는 타입 비교를 수행한다.", "차이가 없다.", "===는 느슨한 비교이다.", 1, "=== 연산자는 암묵적 타입 변환 없이 타입과 값을 모두 비교합니다.", "JS,StrictEquals"],
    ["자바스크립트에서 NaN (Not a Number)의 데이터 타입(typeof NaN)은?", "", "EASY", 35, "\"number\"", "\"nan\"", "\"undefined\"", "\"object\"", 1, "NaN은 숫자로 표현할 수 없는 상태를 나타내는 number 타입 값입니다.", "JS,NaN"]
])

make_qs("JS", "함수", [
    ["화살표 함수(Arrow Function)에 대한 설명으로 올바르지 않은 것은?", "", "MEDIUM", 50, "문법이 간결하다.", "자신만의 this 바인딩을 가지지 않는다.", "생성자 함수로 사용할 수 있다 (new 연산자 사용).", "arguments 객체를 가지지 않는다.", 3, "화살표 함수는 prototype 프로퍼티가 없어 new 연산자로 인스턴스를 생성할 수 없습니다.", "JS,ArrowFunction"],
    ["외부 함수의 변수에 접근할 수 있는 내부 함수와 그 실행 환경의 조합을 의미하는 용어는?", "", "HARD", 65, "클로저 (Closure)", "콜백 (Callback)", "프로토타입 (Prototype)", "프라미스 (Promise)", 1, "클로저는 상태를 안전하게 은닉하고 유지할 때 자주 사용됩니다.", "JS,Closure"],
    ["함수의 매개변수에 기본값을 설정하는 ES6 문법 예시로 올바른 것은?", "", "EASY", 35, "function add(a = 0, b = 0) {}", "function add(a || 0, b || 0) {}", "function add(a : 0, b : 0) {}", "function add(a == 0, b == 0) {}", 1, "매개변수 선언 시 = 연산자를 사용해 기본값을 제공합니다.", "JS,DefaultParam"],
    ["Rest 파라미터(...)의 역할로 올바른 것은?", "", "EASY", 40, "인수들의 목록을 하나의 배열로 받는다.", "배열을 개별 요소로 펼친다.", "함수를 즉시 실행한다.", "객체를 복사한다.", 1, "Rest 파라미터는 개수 지정 없는 가변 인수를 배열로 수집합니다.", "JS,RestParam"],
    ["선언되자마자 즉시 실행되는 함수 형태(IIFE)의 문법으로 올바른 것은?", "", "MEDIUM", 50, "(function() { ... })();", "function() { ... }();", "execute function() { ... }", "new Function()()", 1, "함수를 괄호로 감싸고 소괄호를 붙여 즉시 호출합니다.", "JS,IIFE"],
    ["함수 호출 시 this를 명시적으로 바인딩하는 메서드가 아닌 것은?", "", "MEDIUM", 50, "call()", "apply()", "bind()", "connect()", 4, "call, apply, bind 메서드가 명시적 this 바인딩에 사용됩니다.", "JS,ThisBinding"],
    ["콜백 함수(Callback Function)의 정의로 올바른 것은?", "", "EASY", 30, "다른 함수의 인수(Argument)로 전달되는 함수", "반환값으로 사용되는 변수", "이벤트 핸들러 전용 함수", "재귀 함수", 1, "다른 함수에 매개변수로 전달되어 추후 호출되는 함수입니다.", "JS,Callback"],
    ["고차 함수(Higher-Order Function)의 특징은?", "", "MEDIUM", 50, "함수를 인수로 받거나 함수를 반환하는 함수", "매개변수가 10개 이상인 함수", "비동기만 처리하는 함수", "재귀 호출만 수행하는 함수", 1, "함수를 값으로 취급하여 전달받거나 반환하는 함수를 의미합니다.", "JS,HigherOrder"],
    ["다음 중 비동기 함수를 선언하기 위해 사용하는 ES2017 키워드는?", "", "EASY", 30, "async", "await", "promise", "defer", 1, "async function 문법을 사용합니다.", "JS,Async"],
    ["재귀 함수(Recursive Function) 작성 시 반드시 포함되어야 하는 요소는?", "", "EASY", 40, "탈출 조건 (Base Case)", "this 바인딩", "화살표 문법", "try-catch 블록", 1, "기저 조건(탈출 조건)이 없으면 스택 오버플로우가 발생합니다.", "JS,Recursion"]
])

make_qs("JS", "이벤트", [
    ["이벤트 버블링(Event Bubbling)의 개념으로 올바른 것은?", "", "MEDIUM", 50, "이벤트가 자식 요소에서 부모 요소로 전파되는 현상", "이벤트가 부모에서 자식으로 내려가는 현상", "이벤트가 발생하지 않는 현상", "이벤트가 무한 반복되는 현상", 1, "자식 요소에서 발생한 이벤트가 DOM 트리를 따라 상위 부모 요소로 전파됩니다.", "JS,Bubbling"],
    ["이벤트의 기본 동작(예: a 태그 이동, form 제출)을 중단시키는 메서드는?", "", "EASY", 35, "event.preventDefault()", "event.stopPropagation()", "event.stopImmediatePropagation()", "event.cancel()", 1, "preventDefault() 메서드는 브라우저의 기본 동작을 막습니다.", "JS,PreventDefault"],
    ["이벤트 전파(버블링/캡처링)를 중단시키는 메서드는?", "", "EASY", 35, "event.preventDefault()", "event.stopPropagation()", "event.halt()", "event.close()", 2, "stopPropagation() 메서드는 이벤트의 다음 상위 전파를 중단시킵니다.", "JS,StopPropagation"],
    ["DOM 요소에 이벤트를 등록할 때 표준적으로 사용하는 메서드는?", "", "EASY", 30, "addEventListener()", "attachEvent()", "onEvent()", "bindEvent()", 1, "element.addEventListener('click', handler) 구문을 사용합니다.", "JS,AddEventListener"],
    ["상위 요소 하나에 이벤트를 등록하여 하위 요소들의 이벤트를 제어하는 패턴은?", "", "HARD", 65, "이벤트 위임 (Event Delegation)", "이벤트 캡처링", "이벤트 훅", "이벤트 루프", 1, "이벤트 위임은 메모리 절약과 동적 요소 처리에 매우 유용합니다.", "JS,Delegation"],
    ["마우스가 특정 요소 위로 올라갔을 때 발생하는 이벤트 이름은?", "", "EASY", 30, "mouseover", "click", "keydown", "change", 1, "mouseover 이벤트가 발생합니다.", "JS,MouseOver"],
    ["키보드를 누르고 뗄 때 발생하는 이벤트 이름은?", "", "EASY", 30, "keyup", "keydown", "keypress", "keyclick", 1, "keyup 이벤트는 키에서 손을 떼었을 때 발생합니다.", "JS,KeyUp"],
    ["form 요소 내부의 input 값이 변경되었을 때(포커스를 잃을 때) 발생하는 이벤트는?", "", "EASY", 30, "change", "input", "submit", "focus", 1, "change 이벤트는 값이 변경되고 포커스가 이동될 때 발생합니다.", "JS,ChangeEvent"],
    ["웹 페이지의 모든 DOM 요소와 리소스(이미지 등)가 완전히 로드되었을 때 발생하는 window 이벤트는?", "", "MEDIUM", 50, "load", "DOMContentLoaded", "ready", "init", 1, "load 이벤트는 모든 리소스 다운로드 완료 시 발생합니다.", "JS,LoadEvent"],
    ["HTML 문서의 DOM 트리 구성만 완료되면 즉시 발생하는 이벤트는?", "", "MEDIUM", 50, "DOMContentLoaded", "load", "ready", "finish", 1, "DOMContentLoaded 이벤트는 CSS/이미지를 기다리지 않고 DOM 파싱 직후 발생합니다.", "JS,DOMContentLoaded"]
])

make_qs("JS", "구문", [
    ["구조 분해 할당(Destructuring Assignment) 예시로 올바른 것은?", "", "EASY", 35, "const { name, age } = person;", "const [ name, age ] = person.values;", "const name, age = person;", "const { name: age } = person;", 1, "객체의 프로퍼티를 개별 변수로 추출하는 문법입니다.", "JS,Destructuring"],
    ["스프레드 연산자(Spread Operator)의 기호로 올바른 것은?", "", "EASY", 25, "...", "&&", "||", "??", 1, "점 세 개(...)를 사용합니다.", "JS,Spread"],
    ["null 병합 연산자(Nullish Coalescing Operator, ??)의 동작 기준은?", "", "MEDIUM", 50, "좌항이 null 또는 undefined일 때만 우항을 반환한다.", "좌항이 false일 때 우항을 반환한다.", "좌항이 0일 때 우항을 반환한다.", "좌항이 빈 문자열일 때 우항을 반환한다.", 1, "??는 falsy값(0, '') 중 null과 undefined에만 반응합니다.", "JS,Nullish"],
    ["옵셔널 체이닝(Optional Chaining, ?.)의 역할은?", "", "EASY", 40, "체인 중간의 평가 대상이 null 또는 undefined인 경우 평가를 멈추고 undefined 반환", "에러를 무조건 발생시킴", "삼항 연산자 대체", "객체를 생성함", 1, "TypeError 방지 및 안전한 프로퍼티 접근을 가능하게 합니다.", "JS,OptionalChaining"],
    ["for...in 문과 for...of 문의 차이점으로 올바른 것은?", "", "MEDIUM", 55, "for...in은 객체의 키(Key) 순회, for...of는 이터러블의 값(Value) 순회", "for...in이 배열 전용이다.", "for...of는 객체 전용이다.", "차이가 없다.", 1, "for...in은 프로퍼티 성분, for...of는 배열/문자열 등의 요소를 순회합니다.", "JS,ForInForOf"],
    ["템플릿 리터럴(Template Literal)의 백틱(`) 내에서 변수를 삽입하는 문법은?", "", "EASY", 30, "${variable}", "#{variable}", "%{variable}", "@{variable}", 1, "${} 문법을 사용합니다.", "JS,TemplateLiteral"],
    ["try...catch 문에서 예외 발생 여부와 상관없이 무조건 마지막에 실행되는 블록은?", "", "EASY", 35, "finally", "always", "then", "complete", 1, "finally 블록은 필수로 실행됩니다.", "JS,Finally"],
    ["자바스크립트의 비동기 처리를 유연하게 작성하도록 도와주는 객체는?", "", "EASY", 40, "Promise", "Callback", "Thread", "Worker", 1, "Promise 객체가 대기, 이행, 거부 상태를 관리합니다.", "JS,Promise"],
    ["Promise 객체의 3가지 상태에 해당하지 않는 것은?", "", "MEDIUM", 45, "Pending", "Fulfilled", "Rejected", "Executing", 4, "Promise의 상태는 Pending, Fulfilled, Rejected 3가지입니다.", "JS,PromiseState"],
    ["다음 중 모듈을 내보낼 때(Export) ES6 표준 키워드는?", "", "EASY", 30, "export", "module.exports", "send", "share", 1, "ES6 모듈 표준에서는 export / import 키워드를 사용합니다.", "JS,Export"]
])

make_qs("JS", "자료구조", [
    ["자바스크립트 기본 Array의 특성으로 올바른 것은?", "", "EASY", 35, "동적 크기를 가지며 다양한 타입의 요소를 함께 담을 수 있다.", "고정된 크기를 가진다.", "단일 타입만 허용한다.", "인덱스 접근이 불가능하다.", 1, "자바스크립트 배열은 동적 객체 구조입니다.", "JS,ArrayType"],
    ["배열의 맨 뒤에 요소를 추가하는 메서드는?", "", "EASY", 30, "push()", "pop()", "unshift()", "shift()", 1, "push() 메서드가 배열 끝에 새 요소를 추가합니다.", "JS,ArrayPush"],
    ["배열의 맨 앞에 요소를 제거하는 메서드는?", "", "EASY", 30, "shift()", "unshift()", "pop()", "splice()", 1, "shift() 메서드는 첫 번째 요소를 제거하고 반환합니다.", "JS,ArrayShift"],
    ["배열 요소를 순회하며 조건에 맞는 새 배열을 필터링하는 고차함수는?", "", "EASY", 35, "filter()", "map()", "reduce()", "forEach()", 1, "filter()는 콜백 함수가 true를 반환하는 요소로 새 배열을 만듭니다.", "JS,ArrayFilter"],
    ["배열 요소를 순회하며 각 요소를 변형한 새 배열을 만드는 고차함수는?", "", "EASY", 35, "map()", "filter()", "some()", "find()", 1, "map() 메서드는 요소를 변환하여 신규 배열을 반환합니다.", "JS,ArrayMap"],
    ["Set 객체의 주요 특징은?", "", "EASY", 35, "중복되지 않는 유일한 값들의 집합", "키-값 쌍의 저장소", "인덱스 기반 순서 저장", "LIFO 스택 구조", 1, "Set은 중복을 허용하지 않는 데이터 집합입니다.", "JS,Set"],
    ["Map 객체와 일반 Object의 차이점으로 올바른 것은?", "", "HARD", 60, "Map은 키 타입으로 모든 데이터 타입(객체 포함)을 사용할 수 있다.", "Object가 더 빠르다.", "Map은 순서를 보장하지 않는다.", "차이가 없다.", 1, "Map은 객체나 함수 등 모든 타입을 Key로 사용 가능합니다.", "JS,MapKey"],
    ["WeakMap의 특징으로 올바른 것은?", "", "HARD", 70, "Key가 반드시 객체(Object)이어야 하며 약한 참조를 하여 가비지 컬렉션의 대상이 된다.", "문자열 Key만 가능", "요소 개수를 size로 조회 가능", "순회가 가능하다", 1, "WeakMap의 키 객체는 참조가 사라지면 가비지 컬렉션에 의해 자동 정리됩니다.", "JS,WeakMap"],
    ["배열의 모든 요소를 하나의 단일 값으로 축약할 때 사용하는 고차함수는?", "", "MEDIUM", 50, "reduce()", "concat()", "join()", "slice()", 1, "reduce() 메서드는 누적값을 계산하여 최종 결과 하나를 생성합니다.", "JS,Reduce"],
    ["기존 배열을 변경하지 않고(immutable) 특정 범위의 요소들을 복사하여 배열로 반환하는 메서드는?", "", "EASY", 40, "slice()", "splice()", "push()", "reverse()", 1, "slice()는 원본을 유지하고 splice()는 원본을 변경합니다.", "JS,SliceVsSplice"]
])

# ================= SPRING (8 units x 10 = 80) =================
make_qs("SPRING", "spring 프레임워크", [
    ["스프링 프레임워크의 핵심 특징인 PoJo(Plain Old Java Object)란?", "", "EASY", 40, "특정 프레임워크에 종속되지 않은 순수한 자바 객체", "스프링 전용 부모 클래스를 상속받은 객체", "EJB 기반 객체", "인터페이스로만 이루어진 객체", 1, "POJO는 특정한 규약이나 클래스에 종속되지 않는 순수한 자바 객체를 뜻합니다.", "Spring,POJO"],
    ["스프링의 삼대 핵심 요소에 해당하지 않는 것은?", "", "EASY", 35, "IoC/DI", "AOP", "PSA (Portable Service Abstraction)", "MVC 패턴 표준화 강제", 4, "스프링의 3대 핵심 삼각형 개념은 IoC/DI, AOP, PSA입니다.", "Spring,Triad"],
    ["스프링 부트(Spring Boot)의 대표적인 장점이 아닌 것은?", "", "EASY", 35, "내장 웹 서버(Tomcat 등) 제공", "Auto Configuration (자동 설정)", "의존성 라이브러리 버전 관리 (Starter)", "자바 소스 코드를 C++로 자동 변환", 4, "스프링 부트는 개발 생산성을 높이는 자바 설정 지원 프레임워크입니다.", "Spring,SpringBoot"],
    ["Spring Boot 프로젝트의 메인 클래스 위에 붙이는 종합 어노테이션은?", "", "EASY", 30, "@SpringBootApplication", "@EnableAutoConfiguration", "@ComponentScan", "@Configuration", 1, "@SpringBootApplication 어노테이션을 붙입니다.", "Spring,SpringBootApp"],
    ["application.properties 또는 application.yml 파일의 용도는?", "", "EASY", 30, "애플리케이션 환경 설정 값 관리", "자바 클래스 정의", "HTML 템플릿 작성", "DB 테이블 생성", 1, "포트 번호, DB 접속 정보 등 애플리케이션 환경을 설정합니다.", "Spring,AppProperties"],
    ["스프링 프레임워크에서 객체의 생성 및 생명주기를 관리하는 주체는?", "", "EASY", 35, "Spring IoC Container (ApplicationContext)", "JVM", "Web Browser", "Operating System", 1, "Spring의 IoC 컨테이너가 빈의 생성 및 관리를 전담합니다.", "Spring,Container"],
    ["스프링이 지원하는 서비스 추상화(PSA)의 대표적인 예시는?", "", "HARD", 65, "Spring Transaction Manager (PlatformTransactionManager)", "Java Reflection", "Servlet API 직접 호출", "System.out.println", 1, "PlatformTransactionManager를 통해 다양한 DB 환경을 단일 인터페이스로 추상화합니다.", "Spring,PSA"],
    ["스프링 프로젝트 빌드 도구로 주로 활용되는 것 2가지는?", "", "EASY", 30, "Maven, Gradle", "npm, yarn", "pip, poetry", "make, cmake", 1, "자바 생태계에서는 Maven과 Gradle을 빌드 도구로 활용합니다.", "Spring,BuildTool"],
    ["스프링 부트 스타터(Starter) 의존성의 역할은?", "", "EASY", 40, "관련된 라이브러리 묶음을 간편하게 가져와버전 관리 통합 제공", "코드 자동 완성", "서버 호스팅", "데이터베이스 자동 생성", 1, "starter 의존성은 필요한 라이브러리 그룹을 한번에 의존성 추가해줍니다.", "Spring,Starter"],
    ["스프링 빈(Bean)의 기본 스코프(Scope)는?", "", "EASY", 30, "singleton", "prototype", "request", "session", 1, "스프링 빈의 기본 스코프는 단 하나의 인스턴스만 공유하는 singleton입니다.", "Spring,Scope"]
])

make_qs("SPRING", "IOC", [
    ["IoC (Inversion of Control, 제어의 역전)의 개념으로 올바른 것은?", "", "EASY", 35, "객체의 생성 및 의존성 관리 주도권이 개발자에서 프레임워크로 넘어감", "개발자가 직접 new 연산자로 모든 객체를 생성 및 연결함", "C언어 형태로 포인터를 다룸", "프로그램이 제어 불가능한 상태가 됨", 1, "제어권이 프레임워크 컨테이너로 넘어가는 현상을 제어의 역전이라 합니다.", "Spring,IoC"],
    ["DI (Dependency Injection, 의존성 주입)의 3가지 방식 중 권장되는 방식은?", "", "MEDIUM", 45, "생성자 주입 (Constructor Injection)", "필드 주입 (@Autowired Field)", "Setter 주입", "메서드 주입", 1, "불변성(final) 보장 및 순환 참조 방지를 위해 생성자 주입이 가장 권장됩니다.", "Spring,DI"],
    ["스프링에서 빈(Bean)을 등록하기 위해 클래스에 붙이는 기본 어노테이션은?", "", "EASY", 30, "@Component", "@Inject", "@Resource", "@Bean", 1, "@Component 및 그 파생 어노테이션(@Service, @Repository 등)을 사용합니다.", "Spring,Component"],
    ["@Configuration 클래스 내에서 메서드 단위로 빈을 직접 등록할 때 사용하는 어노테이션은?", "", "EASY", 35, "@Bean", "@Component", "@Service", "@Register", 1, "@Configuration 클래스의 메서드에 @Bean을 붙여 객체를 빈으로 등록합니다.", "Spring,BeanAnno"],
    ["동일한 타입의 빈이 2개 이상 있을 때 특정 빈의 이름을 지정하여 주입받도록 돕는 어노테이션은?", "", "MEDIUM", 50, "@Qualifier", "@Primary", "@Resource", "@Autowired", 1, "@Qualifier(\"빈이름\") 구문을 사용해 주입 대상을 명시합니다.", "Spring,Qualifier"],
    ["동일한 타입의 빈 중 최우선적으로 주입되도록 지정하는 어노테이션은?", "", "EASY", 40, "@Primary", "@Qualifier", "@First", "@Main", 1, "@Primary 어노테이션이 설정된 빈이 우선순위를 가집니다.", "Spring,Primary"],
    ["스프링 빈의 생명주기(Lifecycle) 콜백 메서드를 지정할 때 사용하는 자바 표준 어노테이션 2가지는?", "", "MEDIUM", 50, "@PostConstruct, @PreDestroy", "@Init, @Destroy", "@Before, @After", "@Start, @Stop", 1, "@PostConstruct와 @PreDestroy 어노테이션을 주로 사용합니다.", "Spring,Lifecycle"],
    ["ApplicationContext와 BeanFactory의 관계는?", "", "MEDIUM", 50, "ApplicationContext가 BeanFactory를 상속받은 상위 기능의 컨테이너이다.", "BeanFactory가 상위 기능이다.", "동일한 클래스이다.", "전혀 관련이 없다.", 1, "ApplicationContext는 BeanFactory에 메시지 다국화, 이벤트 송수신 등의 기능을 추가한 인터페이스입니다.", "Spring,ApplicationContext"],
    ["Lombok 라이브러리를 이용하여 생성자 주입 코드를 자동으로 만들어주는 어노테이션은?", "", "EASY", 35, "@RequiredArgsConstructor", "@AllArgsConstructor", "@NoArgsConstructor", "@Data", 1, "@RequiredArgsConstructor는 final 필드에 대해 생성자를 자동 생성합니다.", "Spring,Lombok"],
    ["스프링 컨테이너에 의해 관리되는 자바 객체를 무엇이라고 부르는가?", "", "EASY", 25, "Spring Bean (스프링 빈)", "Spring Entity", "Spring DTO", "Spring Servlet", 1, "스프링 컨테이너가 관리하는 객체를 빈(Bean)이라고 합니다.", "Spring,Bean"]
])

make_qs("SPRING", "AOP", [
    ["AOP (Aspect-Oriented Programming, 관점 지향 프로그래밍)의 핵심 목적은?", "", "EASY", 40, "핵심 비즈니스 로직과 공통 관심 사항(Cross-cutting Concerns)의 분리", "객체지향 프로그래밍 대체", "DB 쿼리 자동화", "UI 디자인 개선", 1, "로깅, 트랜잭션, 보안 등 공통 모듈을 비즈니스 로직과 분리하는 기법입니다.", "Spring,AOP"],
    ["AOP 용어 중 '공통 기능이 적용될 위치(메서드 조인포인트)'를 선정한 표현식 명칭은?", "", "HARD", 60, "Pointcut (포인트컷)", "Advice (어드바이스)", "Aspect (애스펙트)", "Target (타겟)", 1, "Pointcut은 어드바이스가 적용될 조인 포인트를 필터링하는 조건식입니다.", "Spring,Pointcut"],
    ["AOP 용어 중 '부가 기능을 담은 실체 모듈'을 의미하는 것은?", "", "MEDIUM", 50, "Advice (어드바이스)", "Pointcut", "JoinPoint", "Weaving", 1, "Advice는 실제로 실행될 부가 기능 로직(Before, After, Around 등)입니다.", "Spring,Advice"],
    ["Target 메서드 실행 전후 및 예외 발생 시까지 전체를 제어할 수 있는 가장 강력한 Advice 타입은?", "", "MEDIUM", 50, "@Around", "@Before", "@AfterReturning", "@AfterThrowing", 1, "@Around 어드바이스는 ProceedingJoinPoint를 통해 실행 시점을 완벽 제어합니다.", "Spring,Around"],
    ["스프링 AOP가 내부적으로 구현되는 기본 기술 방식은?", "", "HARD", 65, "동적 프록시 (Dynamic Proxy / CGLIB)", "바이트코드 직접 수정", "컴파일 타임 위빙", "JVM 수정", 1, "스프링 AOP는 JDK Dynamic Proxy 및 CGLIB를 이용한 프록시 패턴으로 동작합니다.", "Spring,Proxy"],
    ["AOP 어노테이션을 사용하기 위해 클래스에 붙이는 어노테이션은?", "", "EASY", 35, "@Aspect", "@AopClass", "@Pointcut", "@Advisor", 1, "@Aspect 어노테이션을 통해 애스펙트 모듈임을 선언합니다.", "Spring,AspectAnno"],
    ["다음 중 공통 관심 사항(Cross-cutting Concern)의 예시로 적절하지 않은 것은?", "", "EASY", 35, "회원 가입 비즈니스 로직", "로깅 (Logging)", "트랜잭션 처리 (Transaction)", "성능 측정 (Profiling)", 1, "회원 가입 자체는 핵심 비즈니스 로직(Core Concern)입니다.", "Spring,Concern"],
    ["Pointcut 표현식에서 execution(* com.example.service.*.*(..)) 의 의미는?", "", "HARD", 70, "com.example.service 패키지 내 모든 클래스의 모든 메서드", "특정 메서드 하나만 지정", "리턴 타입이 void인 메서드만 지정", "생성자만 지정", 1, "해당 패키지 아래의 모든 메서드 실행 지점을 의미합니다.", "Spring,PointcutExpr"],
    ["어드바이스가 적용되는 위치(메서드 호출, 객체 생성 등)를 가리키는 용어는?", "", "MEDIUM", 50, "Join Point (조인 포인트)", "Aspect", "Weaving", "Target", 1, "Join Point는 프레임워크가 AOP를 적용할 수 있는 지점들을 의미합니다.", "Spring,JoinPoint"],
    ["Aspect를 Target 객체에 적용하여 프록시 객체를 생성하는 과정을 무엇이라 하는가?", "", "HARD", 65, "Weaving (위빙)", "Injecting", "Linking", "Compiling", 1, "위빙(Weaving)은 포인트컷에 지정된 타겟에 애스펙트를 연결하는 과정입니다.", "Spring,Weaving"]
])

make_qs("SPRING", "ORM", [
    ["자바의 ORM (Object-Relational Mapping) 표준 기술 명세는?", "", "EASY", 30, "JPA (Java Persistence API)", "MyBatis", "JDBC", "Hibernate", 1, "JPA는 자바 진영의 ORM 표준 인터페이스 명세입니다.", "Spring,JPA"],
    ["JPA의 대표적인 구현체(Implementation) 라이브러리는?", "", "EASY", 30, "Hibernate", "Spring Data", "iBatis", "QueryDSL", 1, "Hibernate가 가장 대표적인 JPA 구현체입니다.", "Spring,Hibernate"],
    ["데이터베이스 테이블과 매핑되는 자바 클래스 위에 붙이는 필수 어노테이션은?", "", "EASY", 30, "@Entity", "@Table", "@Column", "@Model", 1, "@Entity 어노테이션을 통해 JPA 매핑 대상임을 나타냅니다.", "Spring,Entity"],
    ["엔티티의 기본키(Primary Key)를 지정할 때 사용하는 어노테이션은?", "", "EASY", 25, "@Id", "@Key", "@PrimaryKey", "@GeneratedValue", 1, "@Id 어노테이션을 사용합니다.", "Spring,Id"],
    ["Spring Data JPA에서 기본 CRUD 메서드를 제공받기 위해 상속받는 인터페이스는?", "", "EASY", 35, "JpaRepository<T, ID>", "CrudInterface", "OrmRepository", "BaseMapper", 1, "JpaRepository<Entity, IdType> 인터페이스를 상속합니다.", "Spring,JpaRepository"],
    ["JPA의 영속성 컨텍스트(Persistence Context)가 제공하는 이점이 아닌 것은?", "", "HARD", 70, "1차 캐시 보장", "동일성(Identity) 보장", "쓰기 지연 (Transactional Write-Behind)", "DB 물리적 서버 자동 증설", 4, "서버 자동 증설은 인프라 영역이며 영속성 컨텍스트의 이점이 아닙니다.", "Spring,PersistenceContext"],
    ["N+1 문제의 발생 원인과 해결 방법으로 가장 올바른 조합은?", "", "HARD", 75, "하위 엔티티 조회 시 N번의 쿼리 추가 발생 / Fetch Join 또는 @EntityGraph 사용", "DB 락 문제 / 트랜잭션 롤백", "메모리 부족 / 캐시 삭제", "PK 중복 / ID 자동증가", 1, "연관관계 조회 시 발생하며 Fetch Join 구문으로 한 번에 조인 조회하여 해결합니다.", "Spring,NPlusOne"],
    ["JPA에서 엔티티의 상태 변화(INSERT/UPDATE/DELETE)를 DB에 실제 반영하는 메서드는?", "", "MEDIUM", 50, "em.flush()", "em.persist()", "em.clear()", "em.detach()", 1, "flush() 메서드는 영속성 컨텍스트의 변경 내용을 데이터베이스에 동기화합니다.", "Spring,Flush"],
    ["Spring Data JPA에서 메서드 이름만으로 쿼리를 자동 생성하는 기능 명칭은?", "", "EASY", 40, "쿼리 메서드 (Query Method)", "JPQL", "Native Query", "Criteria", 1, "findByUsernameAndAge처럼 메서드 명명 규칙으로 쿼리를 만듭니다.", "Spring,QueryMethod"],
    ["JPA 연관관계 매핑 중 1:N 관계를 표현할 때 사용하는 어노테이션은?", "", "EASY", 30, "@OneToMany", "@ManyToOne", "@OneToOne", "@ManyToMany", 1, "@OneToMany 어노테이션을 매핑합니다.", "Spring,OneToMany"]
])

make_qs("SPRING", "Annotation", [
    ["스프링 MVC에서 해당 클래스가 웹 요청을 처리하는 컨트롤러임을 나타내는 어노테이션은?", "", "EASY", 30, "@Controller", "@Service", "@Repository", "@Component", 1, "@Controller 어노테이션을 지정합니다.", "Spring,Controller"],
    ["RESTful 웹 서비스를 제공하며 JSON 형태로 응답을 직접 반환하는 컨트롤러 어노테이션은?", "", "EASY", 30, "@RestController", "@Controller", "@ResponseBodyController", "@WebController", 1, "@RestController는 @Controller + @ResponseBody 기능이 합쳐진 것입니다.", "Spring,RestController"],
    ["클라이언트의 HTTP GET 요청을 처리할 메서드에 붙이는 어노테이션은?", "", "EASY", 25, "@GetMapping", "@PostMapping", "@PutMapping", "@DeleteMapping", 1, "@GetMapping(\"/url\") 구문을 사용합니다.", "Spring,GetMapping"],
    ["URL 경로에 포함된 변수(예: /users/{id})의 값을 파라미터로 추출하는 어노테이션은?", "", "EASY", 35, "@PathVariable", "@RequestParam", "@RequestBody", "@ModelAttribute", 1, "@PathVariable(\"id\") 어노테이션을 사용합니다.", "Spring,PathVariable"],
    ["HTTP 요청의 Body에 담긴 JSON 데이터를 자바 객체로 변환받는 어노테이션은?", "", "EASY", 35, "@RequestBody", "@ResponseBody", "@RequestParam", "@ModelAttribute", 1, "@RequestBody가 JSON을 Jackson 라이브러리를 통해 자바 DTO로 변환합니다.", "Spring,RequestBody"],
    ["HTTP 요청 파라미터(쿼리 스트링 또는 Form 데이터)를 전달받을 때 사용하는 어노테이션은?", "", "EASY", 35, "@RequestParam", "@RequestBody", "@PathVariable", "@Header", 1, "@RequestParam(\"name\") 형태를 사용합니다.", "Spring,RequestParam"],
    ["선언적 트랜잭션 처리를 위해 서비스 메서드 또는 클래스 위에 붙이는 어노테이션은?", "", "EASY", 30, "@Transactional", "@EnableTransaction", "@Tx", "@Commit", 1, "@Transactional 어노테이션을 부여합니다.", "Spring,Transactional"],
    ["스프링의 서비스 계층(Business Logic) 비즈니스 모듈에 붙이는 어노테이션은?", "", "EASY", 25, "@Service", "@Repository", "@Controller", "@Component", 1, "@Service 어노테이션을 붙여 명시합니다.", "Spring,Service"],
    ["데이터 Access 계층(DAO 또는 Repository) 클래스에 붙이는 어노테이션은?", "", "EASY", 25, "@Repository", "@Service", "@Controller", "@Data", 1, "@Repository 어노테이션을 붙이며 DB 예외 추상화 변환을 지원합니다.", "Spring,Repository"],
    ["스프링 환경에서 외부 설정 파일의 값을 자바 변수에 주입받을 때 쓰는 어노테이션은?", "", "MEDIUM", 45, "@Value(\"${property.key}\")", "@Property", "@Config", "@Inject", 1, "@Value 어노테이션을 사용하여 application.yml 속성을 주입받습니다.", "Spring,Value"]
])

make_qs("SPRING", "security", [
    ["Spring Security의 기본 동작 원리 메커니즘은?", "", "MEDIUM", 50, "서블릿 필터 체인 (Servlet Filter Chain)", "AOP 위빙", "인터셉터 (HandlerInterceptor)", "DB 트리거", 1, "Spring Security는 DelegatingFilterProxy 기반의 필터 체인으로 구동됩니다.", "Spring,SecurityFilter"],
    ["사용자의 신원(아이디/비밀번호)을 확인하는 과정을 무엇이라 하는가?", "", "EASY", 30, "인증 (Authentication)", "인가 (Authorization)", "암호화 (Encryption)", "세션 만료", 1, "신원을 확인하는 과정을 인증(Authentication)이라 합니다.", "Spring,Authentication"],
    ["인증된 사용자가 특정 리소스에 접근할 권한이 있는지 확인하는 과정은?", "", "EASY", 30, "인가 (Authorization)", "인증 (Authentication)", "토큰 발행", "해싱", 1, "권한 유무를 검증하는 단계를 인가(Authorization)라 합니다.", "Spring,Authorization"],
    ["사용자 정보를 DB에서 조회하여 UserDetails 객체로 반환하는 커스텀 서비스 인터페이스는?", "", "MEDIUM", 55, "UserDetailsService", "AuthenticationProvider", "SecurityContextHolder", "PasswordEncoder", 1, "UserDetailsService의 loadUserByUsername() 메서드를 구현해야 합니다.", "Spring,UserDetailsService"],
    ["비밀번호를 안전하게 단방향 해시 암호화하기 위해 스프링 세큐리티가 제공하는 표준 암호화 클래스는?", "", "EASY", 35, "BCryptPasswordEncoder", "MD5PasswordEncoder", "SHA1Encoder", "PlainTextEncoder", 1, "BCryptPasswordEncoder가 표준으로 가장 널리 권장됩니다.", "Spring,BCrypt"],
    ["웹 애플리케이션 보안 공격 중 사이트 간 요청 위조 공격 방어를 나타내는 키워드는?", "", "EASY", 40, "CSRF (Cross-Site Request Forgery)", "XSS", "SQL Injection", "CORS", 1, "CSRF 방어 토큰을 생성하여 비인가 요청을 차단합니다.", "Spring,CSRF"],
    ["현재 인증된 사용자의 보안 컨텍스트(Authentication 객체)가 저장되는 공간은?", "", "HARD", 65, "SecurityContextHolder", "HttpSession", "ServletConfig", "ApplicationContext", 1, "SecurityContextHolder -> SecurityContext -> Authentication 구조로 저장됩니다.", "Spring,SecurityContext"],
    ["REST API 환경에서 무상태(Stateless) 인증을 위해 가장 흔히 쓰이는 토큰 방식은?", "", "EASY", 30, "JWT (JSON Web Token)", "JSESSIONID", "Cookie", "OAuth1", 1, "JWT 토큰을 사용하여 세션 없이 인증 상태를 처리합니다.", "Spring,JWT"],
    ["다른 출처(Origin)의 리소스 요청을 허용/제한하는 웹 보안 정책은?", "", "EASY", 35, "CORS (Cross-Origin Resource Sharing)", "CSRF", "XSS", "SSRF", 1, "CORS 설정을 통해 프론트엔드 도메인의 접근을 허용합니다.", "Spring,CORS"],
    ["Spring Security 설정 클래스를 정의할 때 등록하는 보안 필터 체인 빈 타입은?", "", "MEDIUM", 55, "SecurityFilterChain", "WebSecurityConfigurer", "AuthenticationManager", "FilterManager", 1, "@Bean SecurityFilterChain filterChain(HttpSecurity http) 형태로 빈을 정의합니다.", "Spring,SecurityFilterChain"]
])

make_qs("SPRING", "restAPI", [
    ["REST (Representational State Transfer)의 기본 구성 요소 3가지에 해당하지 않는 것은?", "", "MEDIUM", 50, "자원 (Resource - URI)", "행위 (Verb - HTTP Method)", "표현 (Representation - JSON/XML)", "프로토콜 (Protocol - TCP/IP 직접 연결)", 4, "REST는 HTTP 프로토콜 표준 자원, 행위, 표현으로 구성됩니다.", "Spring,REST"],
    ["리소스를 생성(Create)할 때 사용하는 HTTP Method는?", "", "EASY", 25, "POST", "GET", "PUT", "DELETE", 1, "POST 메서드가 생성 요청에 활용됩니다.", "Spring,HttpPost"],
    ["리소스를 수정/교체(Update)할 때 사용하는 HTTP Method는?", "", "EASY", 25, "PUT / PATCH", "GET", "POST", "OPTION", 1, "전체 수정은 PUT, 부분 수정은 PATCH를 사용합니다.", "Spring,HttpPut"],
    ["REST API 응답 성공 시 반환하는 대표적인 HTTP Status Code는?", "", "EASY", 25, "200 OK (또는 201 Created)", "400 Bad Request", "404 Not Found", "500 Server Error", 1, "200 OK 및 201 Created 가 성공 상태 코드입니다.", "Spring,Status200"],
    ["요청한 리소스를 찾을 수 없을 때 반환하는 HTTP Status Code는?", "", "EASY", 25, "404 Not Found", "401 Unauthorized", "403 Forbidden", "500 Internal Error", 1, "404 Not Found 상태 코드입니다.", "Spring,Status404"],
    ["인증되지 않은 사용자의 접근 시 반환하는 HTTP Status Code는?", "", "EASY", 30, "401 Unauthorized", "403 Forbidden", "400 Bad Request", "502 Bad Gateway", 1, "401 Unauthorized가 인증 실패 상태 코드입니다.", "Spring,Status401"],
    ["스프링에서 REST 응답 데이터와 HTTP 헤더, 상태코드를 모두 포함하여 반환할 수 있는 객체는?", "", "EASY", 35, "ResponseEntity<T>", "HttpEntity<T>", "RestResponse", "ModelAndView", 1, "ResponseEntity.ok().body(data) 구조로 사용합니다.", "Spring,ResponseEntity"],
    ["스프링 부트에서 JSON 직렬화/역직렬화를 담당하는 기본 라이브러리는?", "", "MEDIUM", 45, "Jackson", "Gson", "FastJson", "SimpleJson", 1, "Jackson 라이브러리가 기본 내장되어 있습니다.", "Spring,Jackson"],
    ["REST API 명세서를 자동 생성 및 시각화해주는 대표적인 도구는?", "", "EASY", 35, "Swagger (Springdoc OpenAPI)", "Postman", "JUnit", "JProfiler", 1, "Swagger/Springdoc을 통해 API 테스트 및 문서를 자동화합니다.", "Spring,Swagger"],
    ["REST API 설계 가이드라인으로 올바르지 않은 것은?", "", "EASY", 35, "URI에 동사보다는 명사를 사용한다.", "자원에 대한 행위는 HTTP Method로 표현한다.", "슬래시(/)는 계층 관계를 나타낸다.", "URI 마지막에 슬래시(/)를 반드시 포함한다.", 4, "URI 마지막에는 슬래시(/)를 포함하지 않는 것이 명세 규칙입니다.", "Spring,RestRule"]
])

make_qs("SPRING", "MVC", [
    ["Spring MVC 패턴의 3가지 구성 요소에 해당하지 않는 것은?", "", "EASY", 25, "Model", "View", "Controller", "Service", 4, "MVC 패턴 기본 구성요소는 Model, View, Controller 3가지입니다.", "Spring,MVC"],
    ["Spring MVC 프론트 컨트롤러 패턴의 핵심 클래스는?", "", "HARD", 60, "DispatcherServlet", "FilterConfig", "HttpServlet", "AppServlet", 1, "DispatcherServlet이 모든 중앙 HTTP 요청을 받아 적절한 컨트롤러로 위임합니다.", "Spring,DispatcherServlet"],
    ["컨트롤러가 반환한 뷰 이름(View Name)을 바탕으로 실제 HTML/JSP 템플릿을 찾아 연결해주는 컴포넌트는?", "", "MEDIUM", 50, "ViewResolver", "HandlerMapping", "HandlerAdapter", "MessageConverter", 1, "ViewResolver가 뷰 이름 앞뒤로 접두사/접미사를 붙여 실제 템플릿을 찾습니다.", "Spring,ViewResolver"],
    ["클라이언트 요청 URL을 분석하여 담당 컨트롤러 메서드를 찾아주는 컴포넌트는?", "", "MEDIUM", 50, "HandlerMapping", "ViewResolver", "DispatcherServlet", "Filter", 1, "HandlerMapping 컴포넌트가 담당 컨트롤러를 매핑해줍니다.", "Spring,HandlerMapping"],
    ["Model 객체의 주요 역할은?", "", "EASY", 30, "컨트롤러에서 처리한 결과 데이터를 View로 전달하기 위한 데이터 담는 상자", "데이터베이스 테이블 정의", "HTTP 헤더 설정", "보안 필터링", 1, "Model 객체는 View에 전달할 데이터를 key-value로 담아 넘겨줍니다.", "Spring,Model"],
    ["Spring Boot에서 권장하는 대표적인 서버 사이드 템플릿 엔진은?", "", "EASY", 30, "Thymeleaf", "JSP", "Velocity", "PHP", 1, "스프링 부트에서는 Thymeleaf가 표준 템플릿 엔진으로 권장됩니다.", "Spring,Thymeleaf"],
    ["컨트롤러에서 데이터와 뷰 이름을 동시에 반환할 때 사용하는 스프링 클래스는?", "", "EASY", 35, "ModelAndView", "ModelMap", "ViewData", "DataContainer", 1, "ModelAndView 객체에 모델 데이터와 뷰 경로를 동시에 설정하여 반환 가능합니다.", "Spring,ModelAndView"],
    ["Spring MVC에서 인터셉터(HandlerInterceptor)가 구동되는 시점이 아닌 것은?", "", "HARD", 65, "preHandle (컨트롤러 실행 전)", "postHandle (컨트롤러 실행 후)", "afterCompletion (뷰 렌더링 완료 후)", "beforeFilter (서블릿 필터 실행 전)", 4, "인터셉터는 DispatcherServlet 내부에서 구동되므로 서블릿 필터 실행 이후 동작합니다.", "Spring,Interceptor"],
    ["HTML Form 태그 제출 시 클라이언트 데이터의 유효성을 검증하기 위해 사용하는 어노테이션은?", "", "EASY", 35, "@Valid (또는 @Validated)", "@Check", "@Verify", "@Test", 1, "@Valid 어노테이션과 Hibernate Validator 제약조건(@NotNull 등)을 조합하여 사용합니다.", "Spring,Valid"],
    ["Validation 검증 결과 에러 정보를 담아 컨트롤러로 전달되는 객체는?", "", "MEDIUM", 45, "BindingResult", "ErrorMap", "ResultStatus", "ValidationError", 1, "@Valid 뒤에 BindingResult 파라미터를 선언하여 에러 내역을 확인합니다.", "Spring,BindingResult"]
])

df = pd.DataFrame(questions)
output_path = "문제은행_샘플데이터_250문항.xlsx"
df.to_excel(output_path, index=False)
print("Successfully generated Excel file at:", output_path)
print("Total rows:", len(df))
