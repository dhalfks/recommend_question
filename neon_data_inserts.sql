--
-- PostgreSQL database dump
--

\restrict EzLu7cDFoqO8hf7qqbthqWUTynWAKyM4s3flsHYB3OZYORjEvSu6hDza8KuhUiB

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.subjects (id, name, description, created_at) VALUES
	(1, 'Python 기초', 'Python 프로그래밍 기초', '2026-07-28 14:58:59.573295'),
	(2, 'JavaScript', 'JavaScript 및 Web 개발', '2026-07-28 14:58:59.573299'),
	(3, 'SQL', '데이터베이스 쿼리', '2026-07-28 14:58:59.5733'),
	(4, 'Java', 'Java 샘플 문제', '2026-07-29 11:38:49.47884'),
	(5, 'Spring', 'Spring 샘플 문제', '2026-07-29 11:38:49.484694');


--
-- Data for Name: code_files; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.code_files (id, file_name, file_path, file_type, file_content, subject_id, uploaded_at) VALUES
	(1, 'PagingHandler.java', 'uploads\PagingHandler.java', 'java', 'package handler;

import domain.PagingVO;

public class PagingHandler {

	private int startPage; //현재 화면에서 보여줄 시작 페이지네이션의 번호
	private int endPage; //현재 화면에서 보여줄 마지막 페이지네이션의 번호
	private boolean prev, next; //이전, 다음 존재 여부
	
	private int totalCount; //총 글수
	private PagingVO pgvo; //pagingVO
	
	public PagingHandler(PagingVO pgvo, int totalCount) {
		this.pgvo = pgvo;
		this.totalCount = totalCount;
		// 페이지번호 / 한 화면의 개시글 수 * 한 화면의 개시글 수
		// 1~10까지는 10, 11~20까지는 20, (5/10)*10 = 10
		// 한 화면에 10개씩 보여짐
		// 한 화면에 보여지는 페이지네이션 마지막 번호 
		this.endPage 
		= (int)Math.ceil(pgvo.getPageNo() / (pgvo.getQty()*1.0))*pgvo.getQty();
		//한 화면에 보여지는 페이지네이션 첫 번호
		this.startPage = this.endPage - 9; 
		int realEndPage = (int)(Math.ceil((totalCount*1.0)/pgvo.getQty())); //페이지네이션의 전체 끝 페이지
		if(realEndPage < this.endPage) {
			this.endPage = realEndPage;
		}
		this.prev = this.startPage > 1; //존재여부
		this.next = this.endPage < realEndPage; 		
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public boolean isPrev() {
		return prev;
	}

	public void setPrev(boolean prev) {
		this.prev = prev;
	}

	public boolean isNext() {
		return next;
	}

	public void setNext(boolean next) {
		this.next = next;
	}

	public int getTotalCount() {
		return totalCount;
	}

	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	public PagingVO getPgvo() {
		return pgvo;
	}

	public void setPgvo(PagingVO pgvo) {
		this.pgvo = pgvo;
	}
	
	
	
}
', 4, '2026-08-02 11:21:55.44365'),
	(2, 'PagingHandler.java', 'uploads\PagingHandler.java', 'java', 'package handler;

import domain.PagingVO;

public class PagingHandler {

	private int startPage; //현재 화면에서 보여줄 시작 페이지네이션의 번호
	private int endPage; //현재 화면에서 보여줄 마지막 페이지네이션의 번호
	private boolean prev, next; //이전, 다음 존재 여부
	
	private int totalCount; //총 글수
	private PagingVO pgvo; //pagingVO
	
	public PagingHandler(PagingVO pgvo, int totalCount) {
		this.pgvo = pgvo;
		this.totalCount = totalCount;
		// 페이지번호 / 한 화면의 개시글 수 * 한 화면의 개시글 수
		// 1~10까지는 10, 11~20까지는 20, (5/10)*10 = 10
		// 한 화면에 10개씩 보여짐
		// 한 화면에 보여지는 페이지네이션 마지막 번호 
		this.endPage 
		= (int)Math.ceil(pgvo.getPageNo() / (pgvo.getQty()*1.0))*pgvo.getQty();
		//한 화면에 보여지는 페이지네이션 첫 번호
		this.startPage = this.endPage - 9; 
		int realEndPage = (int)(Math.ceil((totalCount*1.0)/pgvo.getQty())); //페이지네이션의 전체 끝 페이지
		if(realEndPage < this.endPage) {
			this.endPage = realEndPage;
		}
		this.prev = this.startPage > 1; //존재여부
		this.next = this.endPage < realEndPage; 		
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public boolean isPrev() {
		return prev;
	}

	public void setPrev(boolean prev) {
		this.prev = prev;
	}

	public boolean isNext() {
		return next;
	}

	public void setNext(boolean next) {
		this.next = next;
	}

	public int getTotalCount() {
		return totalCount;
	}

	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	public PagingVO getPgvo() {
		return pgvo;
	}

	public void setPgvo(PagingVO pgvo) {
		this.pgvo = pgvo;
	}
	
	
	
}
', 4, '2026-08-02 11:31:46.974579');


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.questions (id, subject_id, question_type, title, content, correct_answer, explanation, difficulty, source_file, options, tags, created_at, updated_at, external_id, subject_code, subject_unit, code_snippet, benchmark_time, correct_option, answer_code_snippet, is_required) VALUES
	(10, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 자바 코드의 실행 결과로 올바른 것은?', '1', '5 % 2는 1이므로 else 문이 실행되어 Odd가 출력됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Even", "Odd", "null", "컴파일 에러"]', 'Java,If-Else', '2026-07-29 11:38:49.623844', '2026-07-29 11:38:49.623848', 1, 'JAVA', '기본구문(조건문, 반복문)', 'int a = 5;
if (a % 2 == 0) {
    System.out.println("Even");
} else {
    System.out.println("Odd");
}', 45, 2, NULL, false),
	(11, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 switch-case 문의 출력 결과는?', '1', 'case 2에 break 문이 없으므로 fall-through가 발생하여 B와 C가 출력됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["B", "BC", "ABC", "BCD"]', 'Java,Switch', '2026-07-29 11:38:49.62385', '2026-07-29 11:38:49.623851', 2, 'JAVA', '기본구문(조건문, 반복문)', 'int num = 2;
switch(num) {
    case 1: System.out.print("A");
    case 2: System.out.print("B");
    case 3: System.out.print("C"); break;
    default: System.out.print("D");
}', 60, 2, NULL, false),
	(12, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 for 문이 종료될 때 sum의 값은?', '0', 'i가 짝수인 2, 4일 때는 continue로 지나치므로 홀수 1 + 3 + 5 = 9가 됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["9", "15", "6", "10"]', 'Java,For', '2026-07-29 11:38:49.623853', '2026-07-29 11:38:49.623854', 3, 'JAVA', '기본구문(조건문, 반복문)', 'int sum = 0;
for(int i = 1; i <= 5; i++) {
    if(i % 2 == 0) continue;
    sum += i;
}', 50, 1, NULL, false),
	(13, 4, 'EXCEL', '기본구문(조건문, 반복문)', 'do-while 문과 while 문의 가장 큰 차이점은 무엇인가?', '0', 'do-while 문은 본문을 실행한 후 조건식을 검사하므로 최소 1회 실행됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["do-while 문은 최소 1회 블록을 실행한다.", "while 문은 무한 루프가 불가능하다.", "do-while 문은 조건식을 작성하지 않는다.", "차이점이 없다."]', 'Java,Loop', '2026-07-29 11:38:49.623856', '2026-07-29 11:38:49.623857', 4, 'JAVA', '기본구문(조건문, 반복문)', NULL, 40, 1, NULL, false),
	(14, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 삼항 연산자 코드의 실행 결과는?', '1', '85는 90 미만, 80 이상이므로 중첩 삼항 연산자에 의해 ''B''가 됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["A", "B", "C", "컴파일 에러"]', 'Java,Operator', '2026-07-29 11:38:49.623858', '2026-07-29 11:38:49.623859', 5, 'JAVA', '기본구문(조건문, 반복문)', 'int score = 85;
char grade = (score >= 90) ? ''A'' : (score >= 80) ? ''B'' : ''C'';
System.out.println(grade);', 45, 2, NULL, false),
	(15, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 중 자바의 식별자 작성 규칙으로 올바르지 않은 것은?', '3', '자바는 대소문자를 엄격히 구분합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["첫 글자로 숫자가 올 수 없다.", "특수문자는 _와 $만 허용된다.", "자바 예약어는 식별자로 사용할 수 없다.", "대소문자를 구분하지 않는다."]', 'Java,Syntax', '2026-07-29 11:38:49.623861', '2026-07-29 11:38:49.623862', 6, 'JAVA', '기본구문(조건문, 반복문)', NULL, 40, 4, NULL, false),
	(16, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 조건식 중 변수 x가 10 이상 20 이하일 때 true가 되는 식은?', '1', '자바에서는 논리 연산자 &&를 사용해 조건식을 연결합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["10 <= x <= 20", "x >= 10 && x <= 20", "x >= 10 || x <= 20", "x >= 10 AND x <= 20"]', 'Java,Logic', '2026-07-29 11:38:49.623863', '2026-07-29 11:38:49.623865', 7, 'JAVA', '기본구문(조건문, 반복문)', NULL, 30, 2, NULL, false),
	(17, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 무한 루프를 만드는 구문 중 틀린 것은?', '2', '자바의 while 문 조건식은 반드시 boolean 타입이어야 하므로 while(1)은 컴파일 에러입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["for(;;)", "while(true)", "while(1)", "do {} while(true)"]', 'Java,Loop', '2026-07-29 11:38:49.623866', '2026-07-29 11:38:49.623867', 8, 'JAVA', '기본구문(조건문, 반복문)', NULL, 35, 3, NULL, false),
	(18, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 코드 실행 시 출력되는 값은?', '1', '후위 증가 연산자(x++)는 y에 x(10)가 대입된 후 x가 11로 증가합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["10 10", "10 11", "11 11", "11 10"]', 'Java,Operator', '2026-07-29 11:38:49.623869', '2026-07-29 11:38:49.62387', 9, 'JAVA', '기본구문(조건문, 반복문)', 'int x = 10;
int y = x++;
System.out.println(y + " " + x);', 50, 2, NULL, false),
	(19, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 중 break 문과 continue 문에 대한 설명으로 올바른 것은?', '2', 'break는 switch문과 반복문을 탈출할 때 사용되며, continue는 다음 회차로 이동합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["break는 루프의 다음 회차로 이동한다.", "continue는 가장 가까운 반복문을 완전히 탈출한다.", "break는 switch문과 반복문에서 모두 사용 가능하다.", "continue는 switch문에서 사용 가능하다."]', 'Java,ControlFlow', '2026-07-29 11:38:49.623871', '2026-07-29 11:38:49.623873', 10, 'JAVA', '기본구문(조건문, 반복문)', NULL, 40, 3, NULL, false),
	(20, 4, 'EXCEL', '객체지향개념', '객체지향 프로그래밍의 4대 특징에 해당하지 않는 것은?', '3', '객체지향 4대 특징은 캡슐화, 상속, 다형성, 추상화입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["캡슐화", "상속", "다형성", "절차성"]', 'Java,OOP', '2026-07-29 11:38:49.623874', '2026-07-29 11:38:49.623875', 11, 'JAVA', '객체지향개념', NULL, 30, 4, NULL, false),
	(21, 4, 'EXCEL', '객체지향개념', '다음 코드의 출력으로 올바른 것은?', '1', '오버라이딩된 메서드는 실제 생성된 객체(Child)의 메서드가 호출됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["Parent", "Child", "컴파일 에러", "런타임 에러"]', 'Java,Polymorphism', '2026-07-29 11:38:49.623876', '2026-07-29 11:38:49.623878', 12, 'JAVA', '객체지향개념', 'class Parent { void show() { System.out.println("Parent"); } }
class Child extends Parent { void show() { System.out.println("Child"); } }
Parent p = new Child(); p.show();', 60, 2, NULL, false),
	(22, 4, 'EXCEL', '객체지향개념', '접근 제어자의 접근 범위가 가장 넓은 것부터 좁은 순서로 바르게 나열된 것은?', '0', 'public > protected > default > private 순입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["public > protected > default > private", "public > default > protected > private", "protected > public > default > private", "public > protected > private > default"]', 'Java,AccessModifier', '2026-07-29 11:38:49.623879', '2026-07-29 11:38:49.62388', 13, 'JAVA', '객체지향개념', NULL, 50, 1, NULL, false),
	(23, 4, 'EXCEL', '객체지향개념', '추상 클래스와 인터페이스에 대한 설명으로 틀린 것은?', '2', '인터페이스의 필드는 static final 상수만 가능합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["추상 클래스는 단일 상속만 가능하다.", "인터페이스는 다중 구현이 가능하다.", "인터페이스는 인스턴스 필드를 선언할 수 있다.", "추상 클래스는 생성자를 가질 수 있다."]', 'Java,Interface', '2026-07-29 11:38:49.623882', '2026-07-29 11:38:49.623883', 14, 'JAVA', '객체지향개념', NULL, 70, 3, NULL, false),
	(24, 4, 'EXCEL', '객체지향개념', '오버로딩(Overloading)의 성립 조건으로 올바른 것은?', '0', '오버로딩은 메서드 이름이 같고 매개변수 시그니처가 달라야 합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["메서드 이름이 같고 매개변수의 개수나 타입이 달라야 한다.", "리턴 타입만 다르면 오버로딩이 성립한다.", "접근 제어자만 다르면 성립한다.", "매개변수 이름이 달라야 한다."]', 'Java,Overloading', '2026-07-29 11:38:49.623884', '2026-07-29 11:38:49.623886', 15, 'JAVA', '객체지향개념', NULL, 50, 1, NULL, false),
	(25, 4, 'EXCEL', '객체지향개념', 'static 키워드에 대한 설명으로 올바르지 않은 것은?', '3', 'static 변수는 클래스의 모든 인스턴스가 공유합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["static 멤버는 클래스 로딩 시 메모리에 할당된다.", "static 메서드 내에서는 인스턴스 변수에 직접 접근할 수 없다.", "객체 생성 없이 호출 가능하다.", "static 변수는 객체마다 독립된 값을 가진다."]', 'Java,Static', '2026-07-29 11:38:49.623887', '2026-07-29 11:38:49.623888', 16, 'JAVA', '객체지향개념', NULL, 40, 4, NULL, false),
	(26, 4, 'EXCEL', '객체지향개념', '자바에서 클래스 상속 및 메서드 재정의를 금지할 때 사용하는 키워드는?', '1', 'final 키워드를 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["static", "final", "abstract", "transient"]', 'Java,Final', '2026-07-29 11:38:49.623889', '2026-07-29 11:38:49.623891', 17, 'JAVA', '객체지향개념', NULL, 30, 2, NULL, false),
	(27, 4, 'EXCEL', '객체지향개념', '생성자(Constructor)에 대한 설명으로 올바른 것은?', '1', '생성자가 정의되어 있지 않으면 기본 생성자가 자동 생성됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["반환 타입으로 void를 지정해야 한다.", "클래스 내에 생성자가 없으면 기본 생성자가 자동 추가된다.", "생성자는 상속된다.", "new 키워드 없이 직접 호출 가능하다."]', 'Java,Constructor', '2026-07-29 11:38:49.623892', '2026-07-29 11:38:49.623893', 18, 'JAVA', '객체지향개념', NULL, 40, 2, NULL, false),
	(28, 4, 'EXCEL', '객체지향개념', 'super() 키워드의 용도로 올바른 것은?', '0', 'super()는 부모 클래스 생성자를 호출합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["부모 클래스의 생성자를 호출한다.", "자신 클래스의 다른 생성자를 호출한다.", "부모 클래스를 인스턴스화한다.", "정적 메서드를 호출한다."]', 'Java,Super', '2026-07-29 11:38:49.623895', '2026-07-29 11:38:49.623896', 19, 'JAVA', '객체지향개념', NULL, 40, 1, NULL, false),
	(29, 4, 'EXCEL', '객체지향개념', '정보 은닉(Data Hiding)을 구현하기 위한 가장 적절한 방법은?', '1', 'private 필드와 public Getter/Setter가 표준입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["필드를 public으로 선언한다.", "필드를 private으로 선언하고 Getter/Setter를 제공한다.", "필드를 static으로 선언한다.", "모든 메서드를 private으로 선언한다."]', 'Java,Encapsulation', '2026-07-29 11:38:49.623897', '2026-07-29 11:38:49.623899', 20, 'JAVA', '객체지향개념', NULL, 40, 2, NULL, false),
	(30, 4, 'EXCEL', '스레드', '자바에서 스레드를 생성하는 두 가지 대표적인 방법은?', '0', 'Thread 상속과 Runnable 구현이 기본 방법입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Thread 클래스 상속 / Runnable 인터페이스 구현", "Object 상속 / Process 구현", "Task 클래스 상속 / Executable 구현", "Stream 상속 / Future 구현"]', 'Java,Thread', '2026-07-29 11:38:49.6239', '2026-07-29 11:38:49.623901', 21, 'JAVA', '스레드', NULL, 40, 1, NULL, false),
	(31, 4, 'EXCEL', '스레드', '스레드를 실행시키기 위해 호출해야 하는 메서드는?', '1', 'start() 메서드를 호출해야 새 스레드의 콜 스택이 생성되고 run()이 실행됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["run()", "start()", "execute()", "init()"]', 'Java,ThreadStart', '2026-07-29 11:38:49.623903', '2026-07-29 11:38:49.623904', 22, 'JAVA', '스레드', NULL, 30, 2, NULL, false),
	(32, 4, 'EXCEL', '스레드', '멀티스레드 환경에서 공유 자원의 동기화를 위해 사용하는 키워드는?', '1', 'synchronized 키워드를 통해 임계 영역을 동기화합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["volatile", "synchronized", "transient", "static"]', 'Java,Synchronized', '2026-07-29 11:38:49.623905', '2026-07-29 11:38:49.623906', 23, 'JAVA', '스레드', NULL, 30, 2, NULL, false),
	(33, 4, 'EXCEL', '스레드', '다음 스레드의 상태 중 일시 정지(Waiting/Timed Waiting) 상태에 해당하지 않는 것은?', '0', 'NEW는 스레드 객체가 생성되었으나 아직 start()가 호출되지 않은 상태입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["NEW", "BLOCKED", "WAITING", "TIMED_WAITING"]', 'Java,ThreadState', '2026-07-29 11:38:49.623908', '2026-07-29 11:38:49.623909', 24, 'JAVA', '스레드', NULL, 50, 1, NULL, false),
	(34, 4, 'EXCEL', '스레드', 'sleep() 메서드에 대한 설명으로 올바른 것은?', '0', 'sleep()은 Thread 클래스의 정적 메서드이며, 락을 유지한 채 일시정지합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Thread의 static 메서드이다.", "락(Lock)을 해제하고 대기한다.", "InterruptedException을 발생시키지 않는다.", "Object 클래스의 메서드이다."]', 'Java,Sleep', '2026-07-29 11:38:49.62391', '2026-07-29 11:38:49.623913', 25, 'JAVA', '스레드', NULL, 40, 1, NULL, false),
	(35, 4, 'EXCEL', '스레드', 'wait()와 notify() 메서드가 속한 클래스는?', '2', 'wait(), notify(), notifyAll()은 Object 클래스에 정의되어 있습니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["Thread", "Runnable", "Object", "Process"]', 'Java,ObjectWait', '2026-07-29 11:38:49.623915', '2026-07-29 11:38:49.623916', 26, 'JAVA', '스레드', NULL, 50, 3, NULL, false),
	(36, 4, 'EXCEL', '스레드', '데드락(Deadlock, 교착상태)이 발생하는 4가지 필요조건에 해당하지 않는 것은?', '2', '비선점(No Preemption)이 조건이며, 선점이 가능하면 데드락이 발생하지 않습니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["상호 배제 (Mutual Exclusion)", "점유와 대기 (Hold and Wait)", "선점 (Preemption)", "순환 대기 (Circular Wait)"]', 'Java,Deadlock', '2026-07-29 11:38:49.623917', '2026-07-29 11:38:49.623919', 27, 'JAVA', '스레드', NULL, 70, 3, NULL, false),
	(37, 4, 'EXCEL', '스레드', 'ThreadLocal 클래스의 주된 용도는?', '1', 'ThreadLocal은 각 스레드별 독립적인 변수 공간을 제공합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["스레드 간 변수 공유", "스레드 단위의 독립적인 변수 저장소 제공", "스레드 개수 제한", "스레드 우선순위 변경"]', 'Java,ThreadLocal', '2026-07-29 11:38:49.62392', '2026-07-29 11:38:49.623922', 28, 'JAVA', '스레드', NULL, 65, 2, NULL, false),
	(38, 4, 'EXCEL', '스레드', 'java.util.concurrent 패키지의 ExecutorService 종료 시 사용하는 메서드는?', '1', 'ExecutorService는 shutdown() 또는 shutdownNow()를 사용해 종료합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["stop()", "shutdown()", "destroy()", "finish()"]', 'Java,ExecutorService', '2026-07-29 11:38:49.623923', '2026-07-29 11:38:49.623925', 29, 'JAVA', '스레드', NULL, 50, 2, NULL, false),
	(39, 4, 'EXCEL', '스레드', 'volatile 키워드의 주요 역할은?', '1', 'volatile은 CPU 캐시가 아닌 메인 메모리 직접 참조를 통해 변수의 가시성을 보장합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["원자성(Atomicity) 보장", "변수의 가시성(Visibility) 보장 (메인 메모리 직접 읽기/쓰기)", "스레드 락 생성", "객체 직렬화 제외"]', 'Java,Volatile', '2026-07-29 11:38:49.623926', '2026-07-29 11:38:49.623928', 30, 'JAVA', '스레드', NULL, 70, 2, NULL, false),
	(40, 4, 'EXCEL', 'Collection Framework', 'Collection 인터페이스를 상속받지 않는 Map 계열 컬렉션은?', '2', 'Map은 Collection 인터페이스를 상속받지 않는 별도의 구조입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["ArrayList", "HashSet", "HashMap", "LinkedList"]', 'Java,Collection', '2026-07-29 11:38:49.623929', '2026-07-29 11:38:49.623931', 31, 'JAVA', 'Collection Framework', NULL, 30, 3, NULL, false),
	(41, 4, 'EXCEL', 'Collection Framework', '다음 중 순서를 유지하고 중복을 허용하는 컬렉션 인터페이스는?', '1', 'List 인터페이스는 순서 유지 및 중복을 허용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Set", "List", "Map", "Queue"]', 'Java,List', '2026-07-29 11:38:49.623932', '2026-07-29 11:38:49.623933', 32, 'JAVA', 'Collection Framework', NULL, 30, 2, NULL, false),
	(42, 4, 'EXCEL', 'Collection Framework', 'List 구현체 중 요소의 삽입/삭제가 빈번할 때 가장 유리한 구조는?', '1', 'LinkedList는 노드 포인터만 변경하므로 중간 삽입/삭제 성능이 우수합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["ArrayList", "LinkedList", "Vector", "ArrayDeque"]', 'Java,LinkedList', '2026-07-29 11:38:49.623935', '2026-07-29 11:38:49.623936', 33, 'JAVA', 'Collection Framework', NULL, 40, 2, NULL, false),
	(43, 4, 'EXCEL', 'Collection Framework', 'Set 구현체 중 요소를 자동으로 정렬하여 저장하는 클래스는?', '2', 'TreeSet은 이진 탐색 트리를 기반으로 요소를 오름차순 정렬 저장합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["HashSet", "LinkedHashSet", "TreeSet", "CopyOnWriteArraySet"]', 'Java,TreeSet', '2026-07-29 11:38:49.623938', '2026-07-29 11:38:49.623939', 34, 'JAVA', 'Collection Framework', NULL, 50, 3, NULL, false),
	(44, 4, 'EXCEL', 'Collection Framework', 'HashMap에서 Key 객체의 중복 판단 시 사용하는 두 메서드는?', '1', 'HashMap은 hashCode() 비교 후 동등할 경우 equals()로 최종 검증합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["toString() & equals()", "hashCode() & equals()", "compareTo() & equals()", "clone() & hashCode()"]', 'Java,HashMap', '2026-07-29 11:38:49.623941', '2026-07-29 11:38:49.623942', 35, 'JAVA', 'Collection Framework', NULL, 60, 2, NULL, false),
	(45, 4, 'EXCEL', 'Collection Framework', 'List의 요소를 정렬할 때 사용하는 Collections 클래스의 메서드는?', '0', 'Collections.sort()를 사용하여 정렬합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Collections.sort()", "Collections.order()", "Collections.arrange()", "Collections.group()"]', 'Java,Collections', '2026-07-29 11:38:49.623944', '2026-07-29 11:38:49.623945', 36, 'JAVA', 'Collection Framework', NULL, 30, 1, NULL, false),
	(46, 4, 'EXCEL', 'Collection Framework', 'Stack 클래스는 LIFO 구조입니다. FIFO 구조를 지원하는 컬렉션 인터페이스는?', '1', 'Queue 인터페이스가 FIFO(First In First Out) 구조입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Set", "Queue", "Map", "List"]', 'Java,Queue', '2026-07-29 11:38:49.623947', '2026-07-29 11:38:49.623948', 37, 'JAVA', 'Collection Framework', NULL, 40, 2, NULL, false),
	(47, 4, 'EXCEL', 'Collection Framework', 'Iterator 인터페이스의 주요 메서드가 아닌 것은?', '3', 'Iterator에는 add() 메서드가 없으며 순회 및 삭제만 제공합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["hasNext()", "next()", "remove()", "add()"]', 'Java,Iterator', '2026-07-29 11:38:49.623949', '2026-07-29 11:38:49.623951', 38, 'JAVA', 'Collection Framework', NULL, 40, 4, NULL, false),
	(48, 4, 'EXCEL', 'Collection Framework', '멀티스레드 환경에서 안전한(Thread-safe) Map 구현체는?', '1', 'ConcurrentHashMap은 세그먼트/버킷 단위 락을 사용하여 멀티스레드 안전을 제공합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["HashMap", "ConcurrentHashMap", "TreeMap", "LinkedHashMap"]', 'Java,ConcurrentHashMap', '2026-07-29 11:38:49.623952', '2026-07-29 11:38:49.623954', 39, 'JAVA', 'Collection Framework', NULL, 50, 2, NULL, false),
	(49, 4, 'EXCEL', 'Collection Framework', 'ArrayList의 기본 초기 용량(Capacity)은 얼마인가?', '1', 'ArrayList의 기본 초기 용량은 10입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["5", "10", "16", "20"]', 'Java,ArrayList', '2026-07-29 11:38:49.623955', '2026-07-29 11:38:49.623957', 40, 'JAVA', 'Collection Framework', NULL, 35, 2, NULL, false),
	(50, 4, 'EXCEL', '자료구조', '배열(Array)의 특징으로 올바르지 않은 것은?', '2', '자바의 기본 배열은 생성 후 크기 변경이 불가능합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["크기가 고정되어 있다.", "인덱스를 통한 접근 속도는 O(1)이다.", "동적으로 크기를 늘릴 수 있다.", "연속된 메모리 공간에 저장된다."]', 'Java,Array', '2026-07-29 11:38:49.623958', '2026-07-29 11:38:49.623959', 41, 'JAVA', '자료구조', NULL, 35, 3, NULL, false),
	(51, 4, 'EXCEL', '자료구조', '스택(Stack) 자료구조의 동작 방식은?', '2', '스택은 LIFO (Last In First Out) 구조입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["FIFO", "LIFO", "FILO 및 LIFO", "Random"]', 'Java,Stack', '2026-07-29 11:38:49.623961', '2026-07-29 11:38:49.623962', 42, 'JAVA', '자료구조', NULL, 30, 3, NULL, false),
	(52, 4, 'EXCEL', '자료구조', '큐(Queue)에서 데이터를 넣는 연산과 빼는 연산의 이름은?', '1', '큐에서는 offer/poll 또는 enqueue/dequeue를 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["push / pop", "offer(enqueue) / poll(dequeue)", "add / remove", "insert / delete"]', 'Java,QueueOps', '2026-07-29 11:38:49.623964', '2026-07-29 11:38:49.623965', 43, 'JAVA', '자료구조', NULL, 40, 2, NULL, false),
	(53, 4, 'EXCEL', '자료구조', '해시 테이블(Hash Table)에서 서로 다른 Key가 동일한 해시 값을 가질 때 발생하는 현상은?', '0', '이를 해시 충돌이라고 부릅니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["해시 충돌 (Hash Collision)", "해시 오버플로우", "null 포인터 에러", "데드락"]', 'Java,Hash', '2026-07-29 11:38:49.623967', '2026-07-29 11:38:49.623968', 44, 'JAVA', '자료구조', NULL, 40, 1, NULL, false),
	(54, 4, 'EXCEL', '자료구조', '이진 탐색 트리(BST)에서 최악의 경우(한쪽으로 치우친 트리) 탐색 시간 복잡도는?', '2', '편향 트리가 될 경우 탐색 시간 복잡도는 O(N)으로 저하됩니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["O(1)", "O(log N)", "O(N)", "O(N^2)"]', 'Java,BST', '2026-07-29 11:38:49.623969', '2026-07-29 11:38:49.623971', 45, 'JAVA', '자료구조', NULL, 65, 3, NULL, false),
	(55, 4, 'EXCEL', '자료구조', '연결 리스트(LinkedList)의 단점으로 올바른 것은?', '1', '임의 접근(Random Access)이 불가하여 N번째 노드 접근 시 차례대로 순회해야 합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["데이터 삽입이 어렵다.", "특정 인덱스 접근 시 O(N)의 시간이 소요된다.", "크기가 고정되어 있다.", "메모리를 재사용할 수 없다."]', 'Java,LinkedListDs', '2026-07-29 11:38:49.623972', '2026-07-29 11:38:49.623974', 46, 'JAVA', '자료구조', NULL, 50, 2, NULL, false),
	(56, 4, 'EXCEL', '자료구조', '그래프(Graph) 탐색 알고리즘 중 큐(Queue)를 활용하는 방식은?', '1', 'BFS는 큐를 활용하여 인접한 노드를 먼저 방문합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["DFS (깊이 우선 탐색)", "BFS (너비 우선 탐색)", "Dijkstra", "Binary Search"]', 'Java,BFS', '2026-07-29 11:38:49.623975', '2026-07-29 11:38:49.623977', 47, 'JAVA', '자료구조', NULL, 50, 2, NULL, false),
	(57, 4, 'EXCEL', '자료구조', '최소 힙(Min Heap)에서 루트 노드가 갖는 값은?', '1', '최소 힙의 루트 노드는 항상 전체 요소 중 최솟값을 유지합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["트리 내의 최댓값", "트리 내의 최솟값", "중간값", "랜덤값"]', 'Java,Heap', '2026-07-29 11:38:49.623978', '2026-07-29 11:38:49.623979', 48, 'JAVA', '자료구조', NULL, 45, 2, NULL, false),
	(58, 4, 'EXCEL', '자료구조', '다음 중 정렬 알고리즘의 평균 시간 복잡도가 O(N log N)인 것은?', '2', '퀵 정렬, 병합 정렬, 힙 정렬의 평균 시간 복잡도는 O(N log N)입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["버블 정렬", "선택 정렬", "퀵 정렬 (Quick Sort)", "삽입 정렬"]', 'Java,Sorting', '2026-07-29 11:38:49.623981', '2026-07-29 11:38:49.623982', 49, 'JAVA', '자료구조', NULL, 50, 3, NULL, false),
	(59, 4, 'EXCEL', '자료구조', '원형 큐(Circular Queue)를 사용하는 주된 이유는?', '1', '선형 큐에서 front가 이동하면서 생기는 앞쪽의 빈 공간을 재사용하기 위해 원형 큐를 사용합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["메모리 무제한 확장", "선형 큐의 메모리 낭비(공간 재사용 불가) 해결", "자동 정렬 기능 제공", "LIFO 구조 구현"]', 'Java,CircularQueue', '2026-07-29 11:38:49.623984', '2026-07-29 11:38:49.623985', 50, 'JAVA', '자료구조', NULL, 60, 2, NULL, false),
	(60, 4, 'EXCEL', '람다/스트림', '자바 8에서 도입된 람다식(Lambda Expression)의 기본 문법 형태는?', '0', '자바 람다식은 (매개변수) -> { 바디 } 문법을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["(매개변수) -> { 바디 }", "(매개변수) => { 바디 }", "function(매개변수) {}", "lambda(매개변수) : 바디"]', 'Java,Lambda', '2026-07-29 11:38:49.623987', '2026-07-29 11:38:49.623988', 51, 'JAVA', '람다/스트림', NULL, 30, 1, NULL, false),
	(61, 4, 'EXCEL', '람다/스트림', '함수형 인터페이스(Functional Interface)의 정의는?', '1', '추상 메서드가 오직 1개인 인터페이스를 의미합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["메서드가 하나도 없는 인터페이스", "추상 메서드가 단 하나만 존재하는 인터페이스", "모든 메서드가 default 메서드인 인터페이스", "static 메서드만 가진 인터페이스"]', 'Java,FunctionalInterface', '2026-07-29 11:38:49.62399', '2026-07-29 11:38:49.623991', 52, 'JAVA', '람다/스트림', NULL, 30, 2, NULL, false),
	(62, 4, 'EXCEL', '람다/스트림', '함수형 인터페이스를 나타내기 위해 붙이는 어노테이션은?', '0', '@FunctionalInterface 어노테이션을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@FunctionalInterface", "@Lambda", "@Stream", "@Function"]', 'Java,Annotation', '2026-07-29 11:38:49.623992', '2026-07-29 11:38:49.623994', 53, 'JAVA', '람다/스트림', NULL, 30, 1, NULL, false),
	(63, 4, 'EXCEL', '람다/스트림', '다음 Stream 연산 중 중간 연산(Intermediate Operation)에 해당하는 것은?', '2', 'filter(), map(), sorted() 등은 Stream을 반환하는 중간 연산입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["forEach()", "collect()", "filter()", "count()"]', 'Java,StreamFilter', '2026-07-29 11:38:49.623995', '2026-07-29 11:38:49.623997', 54, 'JAVA', '람다/스트림', NULL, 50, 3, NULL, false),
	(64, 4, 'EXCEL', '람다/스트림', '다음 Stream 연산 중 최종 연산(Terminal Operation)에 해당하는 것은?', '2', 'collect(), forEach(), count() 등은 결과를 도출하는 최종 연산입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["map()", "distinct()", "collect()", "limit()"]', 'Java,StreamCollect', '2026-07-29 11:38:49.623998', '2026-07-29 11:38:49.624', 55, 'JAVA', '람다/스트림', NULL, 50, 3, NULL, false),
	(65, 4, 'EXCEL', '람다/스트림', '다음 코드의 실행 결과 출력되는 값은?', '0', '짝수인 2, 4만 필터링되어 합산되면 6이 됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["6", "15", "9", "3"]', 'Java,StreamExam', '2026-07-29 11:38:49.624001', '2026-07-29 11:38:49.624003', 56, 'JAVA', '람다/스트림', 'List<Integer> list = List.of(1, 2, 3, 4, 5);
int sum = list.stream().filter(n -> n % 2 == 0).mapToInt(n -> n).sum();
System.out.println(sum);', 60, 1, NULL, false),
	(66, 4, 'EXCEL', '람다/스트림', 'Optional 클래스의 용도로 올바른 것은?', '0', 'NullPointerException 예방 및 세련된 null 처리를 위해 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["NullPointerException을 방지하고 null 가능성을 명시적으로 표현", "성능 향상", "멀티스레드 동기화", "데이터 암호화"]', 'Java,Optional', '2026-07-29 11:38:49.624004', '2026-07-29 11:38:49.624005', 57, 'JAVA', '람다/스트림', NULL, 40, 1, NULL, false),
	(67, 4, 'EXCEL', '람다/스트림', '메서드 참조(Method Reference)의 올바른 표현식은?', '0', '클래스명::메서드명 형태로 작성합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["String::valueOf", "String->valueOf", "String.valueOf()", "String@valueOf"]', 'Java,MethodReference', '2026-07-29 11:38:49.624007', '2026-07-29 11:38:49.624008', 58, 'JAVA', '람다/스트림', NULL, 35, 1, NULL, false),
	(68, 4, 'EXCEL', '람다/스트림', '자바의 표준 함수형 인터페이스 중 매개변수가 있고 반환값이 boolean인 것은?', '2', 'Predicate<T>는 T를 받아 boolean을 반환하는 test() 메서드를 가집니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["Consumer<T>", "Supplier<T>", "Predicate<T>", "Function<T, R>"]', 'Java,Predicate', '2026-07-29 11:38:49.62401', '2026-07-29 11:38:49.624011', 59, 'JAVA', '람다/스트림', NULL, 60, 3, NULL, false),
	(69, 4, 'EXCEL', '람다/스트림', 'Stream의 map()과 flatMap()의 차이점은?', '0', 'flatMap은 요소를 스트림으로 변환 후 하나로 합쳐 평평하게 만듭니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["map은 1:1 변환, flatMap은 중첩 구조를 평평하게(1:N) 변환", "map은 최종연산, flatMap은 중간연산", "차이가 없다.", "map은 정수형만 가능"]', 'Java,FlatMap', '2026-07-29 11:38:49.624013', '2026-07-29 11:38:49.624014', 60, 'JAVA', '람다/스트림', NULL, 70, 1, NULL, false),
	(70, 3, 'EXCEL', '기본 SQL 개념', '관계형 데이터베이스(RDBMS)의 특징이 아닌 것은?', '3', 'Key-Value 방식은 NoSQL의 대표적인 특징입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["데이터를 테이블(Table) 형태로 관리한다.", "SQL 언어를 사용하여 제어한다.", "데이터 간의 관계(Relationship)를 정의한다.", "키-값(Key-Value) 쌍으로만 저장된다."]', 'SQL,RDBMS', '2026-07-29 11:38:49.624017', '2026-07-29 11:38:49.624018', 61, 'SQL', '기본 SQL 개념', NULL, 30, 4, NULL, false),
	(71, 3, 'EXCEL', '기본 SQL 개념', '다음 중 데이터의 중복을 제거하고 조회할 때 사용하는 SQL 키워드는?', '1', 'DISTINCT 키워드는 조회 결과에서 중복행을 제거합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["UNIQUE", "DISTINCT", "GROUP BY", "ORDER BY"]', 'SQL,Distinct', '2026-07-29 11:38:49.624019', '2026-07-29 11:38:49.624021', 62, 'SQL', '기본 SQL 개념', NULL, 30, 2, NULL, false),
	(72, 3, 'EXCEL', '기본 SQL 개념', 'NULL 값과의 연산 결과로 올바른 것은?', '1', 'NULL과의 산술 연산 결과는 항상 NULL입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["0", "NULL", "공백", "오류 발생"]', 'SQL,Null', '2026-07-29 11:38:49.624022', '2026-07-29 11:38:49.624023', 63, 'SQL', '기본 SQL 개념', NULL, 35, 2, NULL, false),
	(73, 3, 'EXCEL', '기본 SQL 개념', 'NULL 값을 다른 값으로 대체할 수 있는 ANSI SQL 표준 함수는?', '2', 'COALESCE 함수는 ANSI SQL 표준 인자 중 첫 번째 non-null 값을 반환합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["NVL", "IFNULL", "COALESCE", "ISNULL"]', 'SQL,Coalesce', '2026-07-29 11:38:49.624024', '2026-07-29 11:38:49.624026', 64, 'SQL', '기본 SQL 개념', NULL, 40, 3, NULL, false),
	(74, 3, 'EXCEL', '기본 SQL 개념', 'ORDER BY 절에서 내림차순 정렬을 지정하는 키워드는?', '1', '내림차순 정렬에는 DESC 키워드를 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["ASC", "DESC", "DOWN", "TOP"]', 'SQL,OrderBy', '2026-07-29 11:38:49.624027', '2026-07-29 11:38:49.624028', 65, 'SQL', '기본 SQL 개념', NULL, 30, 2, NULL, false),
	(75, 3, 'EXCEL', '기본 SQL 개념', 'WHERE 절에서 특정 패턴(와일드카드 문자 %, _)을 검색할 때 사용하는 연산자는?', '0', 'LIKE 연산자를 패턴 매칭에 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["LIKE", "MATCH", "IN", "BETWEEN"]', 'SQL,Like', '2026-07-29 11:38:49.624029', '2026-07-29 11:38:49.624031', 66, 'SQL', '기본 SQL 개념', NULL, 30, 1, NULL, false),
	(76, 3, 'EXCEL', '기본 SQL 개념', 'HAVING 절에 대한 설명으로 올바른 것은?', '1', 'HAVING 절은 GROUP BY 결과 집계에 대한 조건을 지정합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["WHERE 절 이전에 실행된다.", "그룹화된 결과(GROUP BY)에 대한 조건 필터링에 사용된다.", "개별 행에 대한 조건을 설정한다.", "ORDER BY 절 다음에 배치된다."]', 'SQL,Having', '2026-07-29 11:38:49.624032', '2026-07-29 11:38:49.624033', 67, 'SQL', '기본 SQL 개념', NULL, 50, 2, NULL, false),
	(77, 3, 'EXCEL', '기본 SQL 개념', '두 테이블을 조인할 때 교집합 영역(공통된 데이터만)을 반환하는 조인 방식은?', '0', 'INNER JOIN은 공통 조건에 일치하는 데이터만 반환합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["INNER JOIN", "LEFT OUTER JOIN", "RIGHT OUTER JOIN", "FULL OUTER JOIN"]', 'SQL,Join', '2026-07-29 11:38:49.624035', '2026-07-29 11:38:49.624036', 68, 'SQL', '기본 SQL 개념', NULL, 35, 1, NULL, false),
	(78, 3, 'EXCEL', '기본 SQL 개념', '기본키(Primary Key)의 두 가지 필수 조건은?', '0', '기본키는 고유성(UNIQUE)과 비어있지 않음(NOT NULL)을 만족해야 합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["NOT NULL & UNIQUE", "NULL 허용 & UNIQUE", "FOREIGN KEY & NOT NULL", "CHECK & DEFAULT"]', 'SQL,PrimaryKey', '2026-07-29 11:38:49.624039', '2026-07-29 11:38:49.62404', 69, 'SQL', '기본 SQL 개념', NULL, 35, 1, NULL, false),
	(79, 3, 'EXCEL', '기본 SQL 개념', '서브쿼리(Subquery) 중 메인쿼리의 컬럼을 참조하여 실행되는 서브쿼리는?', '1', '상관 서브쿼리는 메인쿼리의 행 데이터를 참조하여 매 행마다 실행되는 서브쿼리입니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["스칼라 서브쿼리", "상관 서브쿼리 (Correlated Subquery)", "인라인 뷰", "중첩 서브쿼리"]', 'SQL,Subquery', '2026-07-29 11:38:49.624041', '2026-07-29 11:38:49.624043', 70, 'SQL', '기본 SQL 개념', NULL, 65, 2, NULL, false),
	(80, 3, 'EXCEL', 'DDL', '다음 중 DDL(Data Definition Language) 명령어에 해당하지 않는 것은?', '3', 'INSERT는 DML(데이터 조작어)에 해당합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CREATE", "ALTER", "DROP", "INSERT"]', 'SQL,DDL', '2026-07-29 11:38:49.624044', '2026-07-29 11:38:49.624046', 71, 'SQL', 'DDL', NULL, 30, 4, NULL, false),
	(81, 3, 'EXCEL', 'DDL', '테이블의 구조(컬럼 추가, 변경 등)를 수정할 때 사용하는 DDL 명령어는?', '2', 'ALTER TABLE 명령어로 테이블 구조를 변경합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["MODIFY", "UPDATE", "ALTER", "CHANGE"]', 'SQL,Alter', '2026-07-29 11:38:49.624047', '2026-07-29 11:38:49.624048', 72, 'SQL', 'DDL', NULL, 30, 3, NULL, false),
	(82, 3, 'EXCEL', 'DDL', 'DROP TABLE과 TRUNCATE TABLE의 차이점으로 올바른 것은?', '0', 'DROP은 테이블 객체 자체를 삭제하고, TRUNCATE는 구조는 남기고 전체 행을 빠르게 삭제합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["DROP은 테이블 구조까지 삭제하고, TRUNCATE는 데이터만 전체 삭제한다.", "TRUNCATE는 롤백이 불가능하나 DROP은 롤백된다.", "DROP은 데이터만 삭제한다.", "차이점이 없다."]', 'SQL,Truncate', '2026-07-29 11:38:49.62405', '2026-07-29 11:38:49.624051', 73, 'SQL', 'DDL', NULL, 50, 1, NULL, false),
	(83, 3, 'EXCEL', 'DDL', '테이블 생성 시 컬럼의 값이 비어있지 않도록 강제하는 제약조건은?', '1', 'NOT NULL 제약조건입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["UNIQUE", "NOT NULL", "CHECK", "DEFAULT"]', 'SQL,NotNull', '2026-07-29 11:38:49.624053', '2026-07-29 11:38:49.624054', 74, 'SQL', 'DDL', NULL, 30, 2, NULL, false),
	(84, 3, 'EXCEL', 'DDL', '외래키(Foreign Key) 제약조건의 역할은?', '1', '외래키는 두 테이블 간의 참조 무결성을 유지합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["테이블 내의 유일성을 보장한다.", "참조 무결성(Referential Integrity)을 유지한다.", "자동 인덱스를 제거한다.", "트랜잭션을 자동으로 종료한다."]', 'SQL,ForeignKey', '2026-07-29 11:38:49.624056', '2026-07-29 11:38:49.624057', 75, 'SQL', 'DDL', NULL, 40, 2, NULL, false),
	(85, 3, 'EXCEL', 'DDL', '기존 테이블의 특정 컬럼에 인덱스(Index)를 생성하는 DDL 구문은?', '0', 'CREATE INDEX 인덱스명 ON 테이블명(컬럼명); 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CREATE INDEX", "ADD INDEX", "ALTER INDEX", "MAKE INDEX"]', 'SQL,CreateIndex', '2026-07-29 11:38:49.624058', '2026-07-29 11:38:49.62406', 76, 'SQL', 'DDL', NULL, 40, 1, NULL, false),
	(86, 3, 'EXCEL', 'DDL', '데이터베이스 내에 존재하는 뷰(View)를 삭제하는 명령어는?', '1', 'DROP VIEW 뷰명; 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["DELETE VIEW", "DROP VIEW", "REMOVE VIEW", "TRUNCATE VIEW"]', 'SQL,DropView', '2026-07-29 11:38:49.624061', '2026-07-29 11:38:49.624063', 77, 'SQL', 'DDL', NULL, 35, 2, NULL, false),
	(87, 3, 'EXCEL', 'DDL', 'CASCADE 옵션의 용도로 올바른 것은?', '0', 'ON DELETE CASCADE는 부모 데이터 삭제 시 자식 데이터도 연쇄 삭제합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["참조하는 상위 테이블 삭제 시 하위 데이터도 함께 삭제한다.", "데이터 삭제를 금지한다.", "임시 테이블을 생성한다.", "제약조건을 비활성화한다."]', 'SQL,Cascade', '2026-07-29 11:38:49.624064', '2026-07-29 11:38:49.624066', 78, 'SQL', 'DDL', NULL, 50, 1, NULL, false),
	(88, 3, 'EXCEL', 'DDL', '새로운 테이블을 만드는 DDL 명령어는?', '0', 'CREATE TABLE 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CREATE TABLE", "MAKE TABLE", "BUILD TABLE", "NEW TABLE"]', 'SQL,CreateTable', '2026-07-29 11:38:49.624067', '2026-07-29 11:38:49.624068', 79, 'SQL', 'DDL', NULL, 25, 1, NULL, false),
	(89, 3, 'EXCEL', 'DDL', 'RENAME 명령어의 주된 목적은?', '0', '테이블이나 객체의 이름을 변경합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["데이터베이스 객체(테이블 등)의 이름을 변경한다.", "컬럼 값들을 변경한다.", "테이블을 복사한다.", "데이터 타입을 변환한다."]', 'SQL,Rename', '2026-07-29 11:38:49.62407', '2026-07-29 11:38:49.624071', 80, 'SQL', 'DDL', NULL, 30, 1, NULL, false),
	(90, 3, 'EXCEL', 'DML', '다음 중 DML(Data Manipulation Language) 명령어로만 묶인 것은?', '0', 'DML은 데이터 조작어로 SELECT, INSERT, UPDATE, DELETE입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["SELECT, INSERT, UPDATE, DELETE", "CREATE, ALTER, DROP, TRUNCATE", "GRANT, REVOKE", "COMMIT, ROLLBACK"]', 'SQL,DML', '2026-07-29 11:38:49.624073', '2026-07-29 11:38:49.624074', 81, 'SQL', 'DML', NULL, 30, 1, NULL, false),
	(91, 3, 'EXCEL', 'DML', '테이블에 새로운 행을 삽입하는 SQL 구문은?', '1', 'INSERT INTO 테이블명 VALUES (...) 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["ADD INTO", "INSERT INTO", "PUT INTO", "APPEND INTO"]', 'SQL,Insert', '2026-07-29 11:38:49.624075', '2026-07-29 11:38:49.624077', 82, 'SQL', 'DML', NULL, 30, 2, NULL, false),
	(92, 3, 'EXCEL', 'DML', '기존 데이터를 수정할 때 사용하는 SQL 구문은?', '1', 'UPDATE 테이블명 SET 컬럼=값 WHERE 조건; 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CHANGE", "UPDATE", "MODIFY", "REPLACE"]', 'SQL,Update', '2026-07-29 11:38:49.624078', '2026-07-29 11:38:49.62408', 83, 'SQL', 'DML', NULL, 30, 2, NULL, false),
	(148, 2, 'EXCEL', '함수', '다음 중 비동기 함수를 선언하기 위해 사용하는 ES2017 키워드는?', '0', 'async function 문법을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["async", "await", "promise", "defer"]', 'JS,Async', '2026-07-29 11:38:49.624225', '2026-07-29 11:38:49.624226', 139, 'JS', '함수', NULL, 30, 1, NULL, false),
	(93, 3, 'EXCEL', 'DML', 'UPDATE 문에서 WHERE 절을 생략할 경우 발생하는 현상은?', '1', 'WHERE 절이 없으면 테이블 전체 행이 수정됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["오류가 발생한다.", "테이블의 모든 행 데이터가 변경된다.", "첫 번째 행만 변경된다.", "아무 일도 일어나지 않는다."]', 'SQL,UpdateWarning', '2026-07-29 11:38:49.624081', '2026-07-29 11:38:49.624083', 84, 'SQL', 'DML', NULL, 35, 2, NULL, false),
	(94, 3, 'EXCEL', 'DML', '테이블에서 조건에 맞는 특정 행을 삭제하는 구문은?', '1', 'DELETE FROM 테이블명 WHERE 조건; 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["REMOVE FROM", "DELETE FROM", "DROP FROM", "CLEAR FROM"]', 'SQL,Delete', '2026-07-29 11:38:49.624084', '2026-07-29 11:38:49.624085', 85, 'SQL', 'DML', NULL, 30, 2, NULL, false),
	(95, 3, 'EXCEL', 'DML', '서브쿼리를 활용하여 조건에 따라 INSERT, UPDATE, DELETE를 한 번에 수행하는 구문은?', '1', 'MERGE INTO 구문을 통해 조건부 저장/수정을 한 번에 처리합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["UPSERT", "MERGE", "JOIN UPDATE", "CROSS DML"]', 'SQL,Merge', '2026-07-29 11:38:49.624087', '2026-07-29 11:38:49.624088', 86, 'SQL', 'DML', NULL, 65, 2, NULL, false),
	(96, 3, 'EXCEL', 'DML', '다음 중 여러 행의 그룹별 통계값(합계, 평균 등)을 구할 때 사용하는 함수가 아닌 것은?', '3', 'LENGTH()는 단일 행 문자열 길이 반환 함수입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["SUM()", "AVG()", "COUNT()", "LENGTH()"]', 'SQL,GroupFunction', '2026-07-29 11:38:49.62409', '2026-07-29 11:38:49.624091', 87, 'SQL', 'DML', NULL, 40, 4, NULL, false),
	(97, 3, 'EXCEL', 'DML', 'WHERE 절과 HAVING 절의 차이점으로 맞는 것은?', '0', 'WHERE 절에서는 SUM(), AVG() 같은 집계함수를 직접 조건으로 쓸 수 없고 HAVING을 써야 합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["WHERE는 집계함수 사용 불가, HAVING은 집계함수 조건에 사용", "WHERE는 GROUP BY 이후 동작", "HAVING은 개별 행 필터링", "차이가 없다."]', 'SQL,WhereVsHaving', '2026-07-29 11:38:49.624093', '2026-07-29 11:38:49.624094', 88, 'SQL', 'DML', NULL, 50, 1, NULL, false),
	(98, 3, 'EXCEL', 'DML', 'INSERT 문 작성 시 컬럼명을 생략할 경우 따라야 하는 규칙은?', '0', '컬럼 리스트를 생략하면 전체 컬럼에 대해 정의된 순서대로 값을 전달해야 합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["모든 컬럼의 값을 테이블 정의 순서대로 전부 입력해야 한다.", "원하는 컬럼만 선택해서 넣을 수 있다.", "자동으로 NULL이 들어간다.", "컴파일 오류가 발생한다."]', 'SQL,InsertRule', '2026-07-29 11:38:49.624097', '2026-07-29 11:38:49.624098', 89, 'SQL', 'DML', NULL, 45, 1, NULL, false),
	(99, 3, 'EXCEL', 'DML', 'SELECT 문에서 결과 데이터의 출력 개수를 제한할 때 사용하는 구문(MySQL/PostgreSQL 기준)은?', '0', 'MySQL과 PostgreSQL에서는 LIMIT 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["LIMIT", "TOP", "ROWNUM", "STOP"]', 'SQL,Limit', '2026-07-29 11:38:49.624099', '2026-07-29 11:38:49.6241', 90, 'SQL', 'DML', NULL, 35, 1, NULL, false),
	(100, 3, 'EXCEL', 'DCL', 'DCL(Data Control Language)의 주요 목적은?', '2', 'DCL은 데이터베이스 접근 권한을 제어합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["데이터베이스 객체 생성", "데이터 조회 및 수정", "사용자 권한 부여 및 회수", "트랜잭션 확정"]', 'SQL,DCL', '2026-07-29 11:38:49.624102', '2026-07-29 11:38:49.624103', 91, 'SQL', 'DCL', NULL, 30, 3, NULL, false),
	(101, 3, 'EXCEL', 'DCL', '사용자에게 특정 권한을 부여할 때 사용하는 DCL 명령어는?', '1', 'GRANT 권한 ON 객체 TO 사용자; 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["GIVE", "GRANT", "ALLOW", "PERMIT"]', 'SQL,Grant', '2026-07-29 11:38:49.624104', '2026-07-29 11:38:49.624106', 92, 'SQL', 'DCL', NULL, 30, 2, NULL, false),
	(102, 3, 'EXCEL', 'DCL', '사용자에게 부여했던 권한을 회수할 때 사용하는 DCL 명령어는?', '0', 'REVOKE 권한 ON 객체 FROM 사용자; 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["REVOKE", "REMOVE", "DENY", "CANCEL"]', 'SQL,Revoke', '2026-07-29 11:38:49.624107', '2026-07-29 11:38:49.624108', 93, 'SQL', 'DCL', NULL, 30, 1, NULL, false),
	(103, 3, 'EXCEL', 'DCL', 'GRANT 문에서 WITH GRANT OPTION의 의미는?', '0', '권한 재부여 권한까지 함께 부여합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["부여받은 권한을 다른 사용자에게 다시 부여할 수 있는 권한을 가진다.", "모든 최고 관리자 권한을 받는다.", "권한이 즉시 취소된다.", "읽기 전용 권한만 허용한다."]', 'SQL,GrantOption', '2026-07-29 11:38:49.624109', '2026-07-29 11:38:49.624111', 94, 'SQL', 'DCL', NULL, 60, 1, NULL, false),
	(104, 3, 'EXCEL', 'DCL', '다음 중 DCL 명령어 세트로만 이루어진 것은?', '0', 'GRANT와 REVOKE가 DCL입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["GRANT, REVOKE", "COMMIT, ROLLBACK", "CREATE, DROP", "INSERT, DELETE"]', 'SQL,DclSet', '2026-07-29 11:38:49.624112', '2026-07-29 11:38:49.624113', 95, 'SQL', 'DCL', NULL, 35, 1, NULL, false),
	(105, 3, 'EXCEL', 'DCL', '데이터베이스 사용자(User)를 생성하는 명령어는?', '0', 'CREATE USER 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CREATE USER", "ADD USER", "MAKE USER", "NEW USER"]', 'SQL,CreateUser', '2026-07-29 11:38:49.624115', '2026-07-29 11:38:49.624116', 96, 'SQL', 'DCL', NULL, 35, 1, NULL, false),
	(106, 3, 'EXCEL', 'DCL', '특정 사용자에게 부여된 권한들을 묶어서 관리하는 역할을 하는 객체는?', '0', 'ROLE(롤)을 생성하여 권한을 그룹 단위로 관리합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["ROLE", "GROUP", "CLUSTER", "SCHEMA"]', 'SQL,Role', '2026-07-29 11:38:49.624117', '2026-07-29 11:38:49.624119', 97, 'SQL', 'DCL', NULL, 50, 1, NULL, false),
	(107, 3, 'EXCEL', 'DCL', 'REVOKE CASCADE 명령의 실행 결과는?', '0', '연쇄적으로 재부여된 권한까지 회수됩니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["해당 사용자의 권한과, 그 사용자가 다른 이에게 부여한 권한까지 연쇄 회수된다.", "오류가 발생하여 취소된다.", "해당 사용자의 데이터가 삭제된다.", "모든 사용자의 권한이 회수된다."]', 'SQL,RevokeCascade', '2026-07-29 11:38:49.62412', '2026-07-29 11:38:49.624121', 98, 'SQL', 'DCL', NULL, 65, 1, NULL, false),
	(108, 3, 'EXCEL', 'DCL', 'DCL과 TCL을 구분할 때, COMMIT과 ROLLBACK은 무슨 언어에 속하는가?', '1', 'COMMIT과 ROLLBACK은 TCL(트랜잭션 제어어)입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["DCL", "TCL (Transaction Control Language)", "DDL", "DML"]', 'SQL,TCL', '2026-07-29 11:38:49.624123', '2026-07-29 11:38:49.624124', 99, 'SQL', 'DCL', NULL, 40, 2, NULL, false);
INSERT INTO public.questions (id, subject_id, question_type, title, content, correct_answer, explanation, difficulty, source_file, options, tags, created_at, updated_at, external_id, subject_code, subject_unit, code_snippet, benchmark_time, correct_option, answer_code_snippet, is_required) VALUES
	(109, 3, 'EXCEL', 'DCL', '데이터베이스 보안 관리 차원에서 최소 권한의 원칙(Principle of Least Privilege)이란?', '0', '보안 사고 예방을 위해 최소한의 권한만 제공합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["사용자에게 업무 수행에 필요한 최소한의 권한만 부여하는 것", "모든 사용자에게 관리자 권한 부여", "권한을 전혀 부여하지 않는 것", "DCL 사용 금지"]', 'SQL,Security', '2026-07-29 11:38:49.624125', '2026-07-29 11:38:49.624127', 100, 'SQL', 'DCL', NULL, 45, 1, NULL, false),
	(110, 3, 'EXCEL', '트랜젝션', '트랜잭션의 4가지 주요 특성(ACID)에 해당하지 않는 것은?', '3', 'ACID는 Atomicity, Consistency, Isolation, Durability(영속성)입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["원자성 (Atomicity)", "일관성 (Consistency)", "격리성 (Isolation)", "가용성 (Availability)"]', 'SQL,ACID', '2026-07-29 11:38:49.624128', '2026-07-29 11:38:49.624129', 101, 'SQL', '트랜젝션', NULL, 30, 4, NULL, false),
	(111, 3, 'EXCEL', '트랜젝션', '트랜잭션 작업이 성공적으로 완료되어 변경 사항을 DB에 최종 반영하는 명령어는?', '0', 'COMMIT 구문으로 데이터를 영구 저장합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["COMMIT", "ROLLBACK", "SAVEPOINT", "CONFIRM"]', 'SQL,Commit', '2026-07-29 11:38:49.62413', '2026-07-29 11:38:49.624132', 102, 'SQL', '트랜젝션', NULL, 30, 1, NULL, false),
	(112, 3, 'EXCEL', '트랜젝션', '트랜잭션 실행 중 오류가 발생하여 작업 전 상태로 되돌리는 명령어는?', '1', 'ROLLBACK 구문으로 트랜잭션을 취소하고 이전 상태로 복구합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["COMMIT", "ROLLBACK", "SAVEPOINT", "CANCEL"]', 'SQL,Rollback', '2026-07-29 11:38:49.624133', '2026-07-29 11:38:49.624134', 103, 'SQL', '트랜젝션', NULL, 30, 2, NULL, false),
	(113, 3, 'EXCEL', '트랜젝션', '트랜잭션 내에서 중간 되돌리기 지점을 지정할 때 사용하는 구문은?', '1', 'SAVEPOINT 지점명; 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CHECKPOINT", "SAVEPOINT", "MARK", "BREAKPOINT"]', 'SQL,Savepoint', '2026-07-29 11:38:49.624136', '2026-07-29 11:38:49.624137', 104, 'SQL', '트랜젝션', NULL, 40, 2, NULL, false),
	(114, 3, 'EXCEL', '트랜젝션', '트랜잭션의 격리 수준(Isolation Level) 중 가장 높은 격리성을 제공하나 성능이 가장 낮아지는 단계는?', '3', 'SERIALIZABLE 단계가 가장 높은 격리성과 안전성을 제공합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"]', 'SQL,IsolationLevel', '2026-07-29 11:38:49.624138', '2026-07-29 11:38:49.624139', 105, 'SQL', '트랜젝션', NULL, 70, 4, NULL, false),
	(115, 3, 'EXCEL', '트랜젝션', '다른 트랜잭션이 커밋하지 않은 미확정 데이터를 읽어오는 현상은?', '0', '이를 Dirty Read 현상이라고 합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["Dirty Read", "Non-Repeatable Read", "Phantom Read", "Lost Update"]', 'SQL,DirtyRead', '2026-07-29 11:38:49.624141', '2026-07-29 11:38:49.624142', 106, 'SQL', '트랜젝션', NULL, 65, 1, NULL, false),
	(116, 3, 'EXCEL', '트랜젝션', '트랜잭션의 원자성(Atomicity)에 대한 가장 적절한 설명은?', '0', '원자성은 All or Nothing 특성을 의미합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["트랜잭션 내의 모든 연산은 전체가 수행되거나 전체가 취소되어야 한다 (All or Nothing).", "트랜잭션은 항상 일관된 상태를 유지한다.", "트랜잭션끼리 서로 간섭할 수 없다.", "결과는 영구 저장된다."]', 'SQL,Atomicity', '2026-07-29 11:38:49.624143', '2026-07-29 11:38:49.624144', 107, 'SQL', '트랜젝션', NULL, 50, 1, NULL, false),
	(117, 3, 'EXCEL', '트랜젝션', '트랜잭션 영속성(Durability)을 보장하기 위해 데이터베이스가 사용하는 기능은?', '0', 'Redo/Undo 로그를 통해 시스템 장애 발생 시 복구하여 영속성을 유지합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["트랜잭션 로그 (Redo/Undo Log)", "메인 메모리 락", "인덱스 파일", "뷰(View)"]', 'SQL,Durability', '2026-07-29 11:38:49.624146', '2026-07-29 11:38:49.624147', 108, 'SQL', '트랜젝션', NULL, 65, 1, NULL, false),
	(118, 3, 'EXCEL', '트랜젝션', '오라클/PostgreSQL 등에서 DDL(CREATE 등) 수행 시 트랜잭션의 동작 방식은?', '0', '대부분의 RDBMS에서 DDL 실행 시 묵시적 커밋(Auto Commit)이 실행됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["자동 커밋(Auto Commit)이 발생한다.", "롤백된다.", "트랜잭션이 중단된다.", "아무 일도 일어나지 않는다."]', 'SQL,AutoCommit', '2026-07-29 11:38:49.624148', '2026-07-29 11:38:49.62415', 109, 'SQL', '트랜젝션', NULL, 55, 1, NULL, false),
	(119, 3, 'EXCEL', '트랜젝션', '동시성 제어(Concurrency Control)를 위해 데이터에 잠금을 거는 기법은?', '0', '로킹(Locking) 기법을 통해 동시 접근 시 일관성을 보호합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["Locking", "Hashing", "Indexing", "Partitioning"]', 'SQL,Locking', '2026-07-29 11:38:49.624151', '2026-07-29 11:38:49.624152', 110, 'SQL', '트랜젝션', NULL, 50, 1, NULL, false),
	(120, 3, 'EXCEL', '프로시저/트리거', '저장 프로시저(Stored Procedure)의 장점이 아닌 것은?', '3', '저장 프로시저는 특정 DBMS 전용 언어(PL/SQL 등)로 작성되므로 DB 독립성이 떨어집니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["네트워크 트래픽 감소", "모듈화 및 재사용 가능", "보안성 향상", "데이터베이스 독립성 확보"]', 'SQL,Procedure', '2026-07-29 11:38:49.624154', '2026-07-29 11:38:49.624155', 111, 'SQL', '프로시저/트리거', NULL, 40, 4, NULL, false),
	(121, 3, 'EXCEL', '프로시저/트리거', '특정 테이블에 DML(INSERT, UPDATE, DELETE) 이벤트가 발생할 때 자동으로 실행되는 프로그램 객체는?', '0', '트리거(Trigger)는 특정 데이터 이벤트에 반응하여 자동 실행됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["트리거 (Trigger)", "프로시저 (Procedure)", "사용자 정의 함수 (User Function)", "뷰 (View)"]', 'SQL,Trigger', '2026-07-29 11:38:49.624156', '2026-07-29 11:38:49.624157', 112, 'SQL', '프로시저/트리거', NULL, 35, 1, NULL, false),
	(122, 3, 'EXCEL', '프로시저/트리거', '트리거 내에서 변경 전 값과 변경 후 값을 참조할 때 사용하는 의사 테이블(Pseudo Table)은?', '0', '트리거 내부에서는 :OLD(수정 전)와 :NEW(수정 후)를 통해 데이터에 접근합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["OLD & NEW", "BEFORE & AFTER", "PREV & NEXT", "SRC & DEST"]', 'SQL,OldNew', '2026-07-29 11:38:49.624159', '2026-07-29 11:38:49.62416', 113, 'SQL', '프로시저/트리거', NULL, 65, 1, NULL, false),
	(123, 3, 'EXCEL', '프로시저/트리거', '저장 프로시저와 사용자 정의 함수(Function)의 결정적인 차이점은?', '0', '함수는 단일 값을 반환하여 SELECT절 등 SQL 문장에 직접 활용될 수 있습니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["함수는 반드시 반환값(RETURN)이 존재하고 SQL 문 내부에서 사용 가능하다.", "프로시저만 매개변수를 가질 수 있다.", "함수는 DML을 자유롭게 실행할 수 있다.", "차이가 없다."]', 'SQL,FunctionVsProc', '2026-07-29 11:38:49.624161', '2026-07-29 11:38:49.624162', 114, 'SQL', '프로시저/트리거', NULL, 55, 1, NULL, false),
	(124, 3, 'EXCEL', '프로시저/트리거', '트리거 사용 시 주의해야 할 사항은?', '0', '트리거는 연쇄 반응으로 인한 디버깅 복잡성과 성능 저하를 일으킬 수 있습니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["무분별한 트리거 사용은 시스템 성능 저하 및 디버깅을 어렵게 만든다.", "트리거는 1개만 생성 가능하다.", "트리거는 파라미터를 입력받을 수 있다.", "트리거는 수동으로만 실행된다."]', 'SQL,TriggerCaution', '2026-07-29 11:38:49.624164', '2026-07-29 11:38:49.624165', 115, 'SQL', '프로시저/트리거', NULL, 65, 1, NULL, false),
	(125, 3, 'EXCEL', '프로시저/트리거', 'PL/SQL 프로시저에서 예외 처리를 담당하는 블록 키워드는?', '0', 'EXCEPTION 블록에서 예외를 처리합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["EXCEPTION", "CATCH", "ERROR", "THROW"]', 'SQL,Exception', '2026-07-29 11:38:49.624166', '2026-07-29 11:38:49.624168', 116, 'SQL', '프로시저/트리거', NULL, 40, 1, NULL, false),
	(126, 3, 'EXCEL', '프로시저/트리거', '프로시저 정의 시 입출력 매개변수 타입을 지정할 때 쓰는 키워드가 아닌 것은?', '3', '프로시저 파라미터 모드는 IN, OUT, INOUT이 있습니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["IN", "OUT", "INOUT", "BOUND"]', 'SQL,ProcedureParam', '2026-07-29 11:38:49.624169', '2026-07-29 11:38:49.62417', 117, 'SQL', '프로시저/트리거', NULL, 50, 4, NULL, false),
	(127, 3, 'EXCEL', '프로시저/트리거', '행 단위로 트리거가 실행되도록 지정하는 트리거 구문 옵션은?', '0', 'FOR EACH ROW 구문을 통해 행 단위 트리거(Row Trigger)를 설정합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["FOR EACH ROW", "FOR EACH TABLE", "EVERY STATEMENT", "PER ROW"]', 'SQL,ForEachRow', '2026-07-29 11:38:49.624171', '2026-07-29 11:38:49.624173', 118, 'SQL', '프로시저/트리거', NULL, 50, 1, NULL, false),
	(128, 3, 'EXCEL', '프로시저/트리거', '트리거가 실행되는 시점을 지정하는 키워드 2가지는?', '0', '이벤트 발생 전(BEFORE) 또는 후(AFTER) 시점을 지정합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["BEFORE / AFTER", "START / END", "FIRST / LAST", "CREATE / DROP"]', 'SQL,TriggerTiming', '2026-07-29 11:38:49.624174', '2026-07-29 11:38:49.624175', 119, 'SQL', '프로시저/트리거', NULL, 40, 1, NULL, false),
	(129, 3, 'EXCEL', '프로시저/트리거', 'PL/SQL의 기본 블록 구조 순서로 올바른 것은?', '0', '선언부(DECLARE) -> 실행부(BEGIN) -> 예외처리부(EXCEPTION) -> 종료(END) 순입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["DECLARE -> BEGIN -> EXCEPTION -> END", "BEGIN -> DECLARE -> END", "START -> PROCESS -> END", "DECLARE -> EXCEPTION -> END"]', 'SQL,PlSqlStructure', '2026-07-29 11:38:49.624177', '2026-07-29 11:38:49.624178', 120, 'SQL', '프로시저/트리거', NULL, 55, 1, NULL, false),
	(130, 2, 'EXCEL', '변수', 'JavaScript에서 블록 스코프(Block Scope)를 가지는 변수 선언 키워드 2가지는?', '0', 'let과 const는 블록 스코프를 지원하며 var는 함수 스코프입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["let, const", "var, let", "var, const", "global, local"]', 'JS,Variable', '2026-07-29 11:38:49.624179', '2026-07-29 11:38:49.62418', 121, 'JS', '변수', NULL, 30, 1, NULL, false),
	(131, 2, 'EXCEL', '변수', 'const 키워드로 선언된 객체의 속성(Property)을 변경할 때 발생하는 현상은?', '0', 'const는 재할당이 금지되지만 참조 객체의 내부 프로퍼티 수정은 가능합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["정상적으로 속성이 변경된다.", "TypeError 오류가 발생한다.", "SyntaxError 오류가 발생한다.", "속성이 무시된다."]', 'JS,ConstObject', '2026-07-29 11:38:49.624182', '2026-07-29 11:38:49.624183', 122, 'JS', '변수', NULL, 50, 1, NULL, false),
	(132, 2, 'EXCEL', '변수', '변수가 선언되기 전에 참조할 때 발생하는 자바스크립트 고유의 동작 메커니즘은?', '0', '선언부가 스코프 상단으로 끌어올려지는 현상을 호이스팅이라고 합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["호이스팅 (Hoisting)", "클로저 (Closure)", "프로토타입 (Prototype)", "이벤트 루프"]', 'JS,Hoisting', '2026-07-29 11:38:49.624184', '2026-07-29 11:38:49.624185', 123, 'JS', '변수', NULL, 40, 1, NULL, false),
	(133, 2, 'EXCEL', '변수', '다음 중 자바스크립트의 원시 타입(Primitive Type)이 아닌 것은?', '3', 'object는 참조 타입(Reference Type)에 속합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["number", "string", "boolean", "object"]', 'JS,Primitive', '2026-07-29 11:38:49.624187', '2026-07-29 11:38:49.624188', 124, 'JS', '변수', NULL, 30, 4, NULL, false),
	(134, 2, 'EXCEL', '변수', 'Symbol 데이터 타입의 주된 용도는?', '0', 'Symbol은 충돌 없는 고유한 키 값을 만들 때 사용됩니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["유일하고 변경 불가능한 고유한 객체 프로퍼티 키 생성", "문자열 결합", "빅인트 연산", "메모리 해제"]', 'JS,Symbol', '2026-07-29 11:38:49.624189', '2026-07-29 11:38:49.624191', 125, 'JS', '변수', NULL, 60, 1, NULL, false),
	(135, 2, 'EXCEL', '변수', 'var 키워드로 선언된 변수의 기본 초기화 값은?', '1', 'var 변수는 호이스팅 시 undefined로 초기화됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["null", "undefined", "0", "false"]', 'JS,VarUndefined', '2026-07-29 11:38:49.624192', '2026-07-29 11:38:49.624193', 126, 'JS', '변수', NULL, 30, 2, NULL, false),
	(136, 2, 'EXCEL', '변수', '다음 중 typeof null 의 실행 결과로 출력되는 것은?', '2', '자바스크립트의 초기 설계 오류로 typeof null은 "object"를 반환합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["\"null\"", "\"undefined\"", "\"object\"", "\"number\""]', 'JS,TypeOfNull', '2026-07-29 11:38:49.624195', '2026-07-29 11:38:49.624196', 127, 'JS', '변수', NULL, 45, 3, NULL, false),
	(137, 2, 'EXCEL', '변수', 'Temporal Dead Zone (TDZ)의 영향을 받는 변수 선언 키워드는?', '1', 'let과 const는 선언 이전에 접근 시 TDZ에 의해 ReferenceError가 발생합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["var", "let, const", "function", "import"]', 'JS,TDZ', '2026-07-29 11:38:49.624197', '2026-07-29 11:38:49.624198', 128, 'JS', '변수', NULL, 65, 2, NULL, false),
	(138, 2, 'EXCEL', '변수', '동등 연산자(==)와 엄격 동등 연산자(===)의 차이점은?', '0', NULL, 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '[null, "#NAME?", "차이가 없다.", null]', 'JS,StrictEquals', '2026-07-29 11:38:49.6242', '2026-07-29 11:38:49.624201', 129, 'JS', '변수', NULL, 30, 1, NULL, false),
	(139, 2, 'EXCEL', '변수', '자바스크립트에서 NaN (Not a Number)의 데이터 타입(typeof NaN)은?', '0', 'NaN은 숫자로 표현할 수 없는 상태를 나타내는 number 타입 값입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["\"number\"", "\"nan\"", "\"undefined\"", "\"object\""]', 'JS,NaN', '2026-07-29 11:38:49.624202', '2026-07-29 11:38:49.624203', 130, 'JS', '변수', NULL, 35, 1, NULL, false),
	(140, 2, 'EXCEL', '함수', '화살표 함수(Arrow Function)에 대한 설명으로 올바르지 않은 것은?', '2', '화살표 함수는 prototype 프로퍼티가 없어 new 연산자로 인스턴스를 생성할 수 없습니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["문법이 간결하다.", "자신만의 this 바인딩을 가지지 않는다.", "생성자 함수로 사용할 수 있다 (new 연산자 사용).", "arguments 객체를 가지지 않는다."]', 'JS,ArrowFunction', '2026-07-29 11:38:49.624205', '2026-07-29 11:38:49.624206', 131, 'JS', '함수', NULL, 50, 3, NULL, false),
	(141, 2, 'EXCEL', '함수', '외부 함수의 변수에 접근할 수 있는 내부 함수와 그 실행 환경의 조합을 의미하는 용어는?', '0', '클로저는 상태를 안전하게 은닉하고 유지할 때 자주 사용됩니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["클로저 (Closure)", "콜백 (Callback)", "프로토타입 (Prototype)", "프라미스 (Promise)"]', 'JS,Closure', '2026-07-29 11:38:49.624207', '2026-07-29 11:38:49.624208', 132, 'JS', '함수', NULL, 65, 1, NULL, false),
	(142, 2, 'EXCEL', '함수', '함수의 매개변수에 기본값을 설정하는 ES6 문법 예시로 올바른 것은?', '0', '매개변수 선언 시 = 연산자를 사용해 기본값을 제공합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["function add(a = 0, b = 0) {}", "function add(a || 0, b || 0) {}", "function add(a : 0, b : 0) {}", "function add(a == 0, b == 0) {}"]', 'JS,DefaultParam', '2026-07-29 11:38:49.62421', '2026-07-29 11:38:49.624211', 133, 'JS', '함수', NULL, 35, 1, NULL, false),
	(143, 2, 'EXCEL', '함수', 'Rest 파라미터(...)의 역할로 올바른 것은?', '0', 'Rest 파라미터는 개수 지정 없는 가변 인수를 배열로 수집합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["인수들의 목록을 하나의 배열로 받는다.", "배열을 개별 요소로 펼친다.", "함수를 즉시 실행한다.", "객체를 복사한다."]', 'JS,RestParam', '2026-07-29 11:38:49.624212', '2026-07-29 11:38:49.624213', 134, 'JS', '함수', NULL, 40, 1, NULL, false),
	(144, 2, 'EXCEL', '함수', '선언되자마자 즉시 실행되는 함수 형태(IIFE)의 문법으로 올바른 것은?', '0', '함수를 괄호로 감싸고 소괄호를 붙여 즉시 호출합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["(function() { ... })();", "function() { ... }();", "execute function() { ... }", "new Function()()"]', 'JS,IIFE', '2026-07-29 11:38:49.624215', '2026-07-29 11:38:49.624216', 135, 'JS', '함수', NULL, 50, 1, NULL, false),
	(145, 2, 'EXCEL', '함수', '함수 호출 시 this를 명시적으로 바인딩하는 메서드가 아닌 것은?', '3', 'call, apply, bind 메서드가 명시적 this 바인딩에 사용됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["call()", "apply()", "bind()", "connect()"]', 'JS,ThisBinding', '2026-07-29 11:38:49.624217', '2026-07-29 11:38:49.624219', 136, 'JS', '함수', NULL, 50, 4, NULL, false),
	(146, 2, 'EXCEL', '함수', '콜백 함수(Callback Function)의 정의로 올바른 것은?', '0', '다른 함수에 매개변수로 전달되어 추후 호출되는 함수입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["다른 함수의 인수(Argument)로 전달되는 함수", "반환값으로 사용되는 변수", "이벤트 핸들러 전용 함수", "재귀 함수"]', 'JS,Callback', '2026-07-29 11:38:49.62422', '2026-07-29 11:38:49.624221', 137, 'JS', '함수', NULL, 30, 1, NULL, false),
	(147, 2, 'EXCEL', '함수', '고차 함수(Higher-Order Function)의 특징은?', '0', '함수를 값으로 취급하여 전달받거나 반환하는 함수를 의미합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["함수를 인수로 받거나 함수를 반환하는 함수", "매개변수가 10개 이상인 함수", "비동기만 처리하는 함수", "재귀 호출만 수행하는 함수"]', 'JS,HigherOrder', '2026-07-29 11:38:49.624222', '2026-07-29 11:38:49.624224', 138, 'JS', '함수', NULL, 50, 1, NULL, false),
	(149, 2, 'EXCEL', '함수', '재귀 함수(Recursive Function) 작성 시 반드시 포함되어야 하는 요소는?', '0', '기저 조건(탈출 조건)이 없으면 스택 오버플로우가 발생합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["탈출 조건 (Base Case)", "this 바인딩", "화살표 문법", "try-catch 블록"]', 'JS,Recursion', '2026-07-29 11:38:49.624228', '2026-07-29 11:38:49.624229', 140, 'JS', '함수', NULL, 40, 1, NULL, false),
	(150, 2, 'EXCEL', '이벤트', '이벤트 버블링(Event Bubbling)의 개념으로 올바른 것은?', '0', '자식 요소에서 발생한 이벤트가 DOM 트리를 따라 상위 부모 요소로 전파됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["이벤트가 자식 요소에서 부모 요소로 전파되는 현상", "이벤트가 부모에서 자식으로 내려가는 현상", "이벤트가 발생하지 않는 현상", "이벤트가 무한 반복되는 현상"]', 'JS,Bubbling', '2026-07-29 11:38:49.62423', '2026-07-29 11:38:49.624231', 141, 'JS', '이벤트', NULL, 50, 1, NULL, false),
	(151, 2, 'EXCEL', '이벤트', '이벤트의 기본 동작(예: a 태그 이동, form 제출)을 중단시키는 메서드는?', '0', 'preventDefault() 메서드는 브라우저의 기본 동작을 막습니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["event.preventDefault()", "event.stopPropagation()", "event.stopImmediatePropagation()", "event.cancel()"]', 'JS,PreventDefault', '2026-07-29 11:38:49.624233', '2026-07-29 11:38:49.624234', 142, 'JS', '이벤트', NULL, 35, 1, NULL, false),
	(152, 2, 'EXCEL', '이벤트', '이벤트 전파(버블링/캡처링)를 중단시키는 메서드는?', '1', 'stopPropagation() 메서드는 이벤트의 다음 상위 전파를 중단시킵니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["event.preventDefault()", "event.stopPropagation()", "event.halt()", "event.close()"]', 'JS,StopPropagation', '2026-07-29 11:38:49.624235', '2026-07-29 11:38:49.624237', 143, 'JS', '이벤트', NULL, 35, 2, NULL, false),
	(153, 2, 'EXCEL', '이벤트', 'DOM 요소에 이벤트를 등록할 때 표준적으로 사용하는 메서드는?', '0', 'element.addEventListener(''click'', handler) 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["addEventListener()", "attachEvent()", "onEvent()", "bindEvent()"]', 'JS,AddEventListener', '2026-07-29 11:38:49.624238', '2026-07-29 11:38:49.624239', 144, 'JS', '이벤트', NULL, 30, 1, NULL, false),
	(154, 2, 'EXCEL', '이벤트', '상위 요소 하나에 이벤트를 등록하여 하위 요소들의 이벤트를 제어하는 패턴은?', '0', '이벤트 위임은 메모리 절약과 동적 요소 처리에 매우 유용합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["이벤트 위임 (Event Delegation)", "이벤트 캡처링", "이벤트 훅", "이벤트 루프"]', 'JS,Delegation', '2026-07-29 11:38:49.62424', '2026-07-29 11:38:49.624242', 145, 'JS', '이벤트', NULL, 65, 1, NULL, false),
	(155, 2, 'EXCEL', '이벤트', '마우스가 특정 요소 위로 올라갔을 때 발생하는 이벤트 이름은?', '0', 'mouseover 이벤트가 발생합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["mouseover", "click", "keydown", "change"]', 'JS,MouseOver', '2026-07-29 11:38:49.624243', '2026-07-29 11:38:49.624244', 146, 'JS', '이벤트', NULL, 30, 1, NULL, false),
	(156, 2, 'EXCEL', '이벤트', '키보드를 누르고 뗄 때 발생하는 이벤트 이름은?', '0', 'keyup 이벤트는 키에서 손을 떼었을 때 발생합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["keyup", "keydown", "keypress", "keyclick"]', 'JS,KeyUp', '2026-07-29 11:38:49.624245', '2026-07-29 11:38:49.624247', 147, 'JS', '이벤트', NULL, 30, 1, NULL, false),
	(157, 2, 'EXCEL', '이벤트', 'form 요소 내부의 input 값이 변경되었을 때(포커스를 잃을 때) 발생하는 이벤트는?', '0', 'change 이벤트는 값이 변경되고 포커스가 이동될 때 발생합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["change", "input", "submit", "focus"]', 'JS,ChangeEvent', '2026-07-29 11:38:49.624248', '2026-07-29 11:38:49.624249', 148, 'JS', '이벤트', NULL, 30, 1, NULL, false),
	(158, 2, 'EXCEL', '이벤트', '웹 페이지의 모든 DOM 요소와 리소스(이미지 등)가 완전히 로드되었을 때 발생하는 window 이벤트는?', '0', 'load 이벤트는 모든 리소스 다운로드 완료 시 발생합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["load", "DOMContentLoaded", "ready", "init"]', 'JS,LoadEvent', '2026-07-29 11:38:49.624251', '2026-07-29 11:38:49.624252', 149, 'JS', '이벤트', NULL, 50, 1, NULL, false),
	(159, 2, 'EXCEL', '이벤트', 'HTML 문서의 DOM 트리 구성만 완료되면 즉시 발생하는 이벤트는?', '0', 'DOMContentLoaded 이벤트는 CSS/이미지를 기다리지 않고 DOM 파싱 직후 발생합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["DOMContentLoaded", "load", "ready", "finish"]', 'JS,DOMContentLoaded', '2026-07-29 11:38:49.624253', '2026-07-29 11:38:49.624254', 150, 'JS', '이벤트', NULL, 50, 1, NULL, false),
	(160, 2, 'EXCEL', '구문', '구조 분해 할당(Destructuring Assignment) 예시로 올바른 것은?', '0', '객체의 프로퍼티를 개별 변수로 추출하는 문법입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["const { name, age } = person;", "const [ name, age ] = person.values;", "const name, age = person;", "const { name: age } = person;"]', 'JS,Destructuring', '2026-07-29 11:38:49.624256', '2026-07-29 11:38:49.624257', 151, 'JS', '구문', NULL, 35, 1, NULL, false),
	(161, 2, 'EXCEL', '구문', '스프레드 연산자(Spread Operator)의 기호로 올바른 것은?', '0', '점 세 개(...)를 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["...", "&&", "||", "??"]', 'JS,Spread', '2026-07-29 11:38:49.624258', '2026-07-29 11:38:49.624259', 152, 'JS', '구문', NULL, 25, 1, NULL, false),
	(162, 2, 'EXCEL', '구문', 'null 병합 연산자(Nullish Coalescing Operator, ??)의 동작 기준은?', '0', '??는 falsy값(0, '''') 중 null과 undefined에만 반응합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["좌항이 null 또는 undefined일 때만 우항을 반환한다.", "좌항이 false일 때 우항을 반환한다.", "좌항이 0일 때 우항을 반환한다.", "좌항이 빈 문자열일 때 우항을 반환한다."]', 'JS,Nullish', '2026-07-29 11:38:49.624261', '2026-07-29 11:38:49.624262', 153, 'JS', '구문', NULL, 50, 1, NULL, false),
	(163, 2, 'EXCEL', '구문', '옵셔널 체이닝(Optional Chaining, ?.)의 역할은?', '0', 'TypeError 방지 및 안전한 프로퍼티 접근을 가능하게 합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["체인 중간의 평가 대상이 null 또는 undefined인 경우 평가를 멈추고 undefined 반환", "에러를 무조건 발생시킴", "삼항 연산자 대체", "객체를 생성함"]', 'JS,OptionalChaining', '2026-07-29 11:38:49.624263', '2026-07-29 11:38:49.624264', 154, 'JS', '구문', NULL, 40, 1, NULL, false),
	(164, 2, 'EXCEL', '구문', 'for...in 문과 for...of 문의 차이점으로 올바른 것은?', '0', 'for...in은 프로퍼티 성분, for...of는 배열/문자열 등의 요소를 순회합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["for...in은 객체의 키(Key) 순회, for...of는 이터러블의 값(Value) 순회", "for...in이 배열 전용이다.", "for...of는 객체 전용이다.", "차이가 없다."]', 'JS,ForInForOf', '2026-07-29 11:38:49.624266', '2026-07-29 11:38:49.624267', 155, 'JS', '구문', NULL, 55, 1, NULL, false),
	(165, 2, 'EXCEL', '구문', '템플릿 리터럴(Template Literal)의 백틱(`) 내에서 변수를 삽입하는 문법은?', '0', '${} 문법을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["${variable}", "#{variable}", "%{variable}", "@{variable}"]', 'JS,TemplateLiteral', '2026-07-29 11:38:49.624268', '2026-07-29 11:38:49.624269', 156, 'JS', '구문', NULL, 30, 1, NULL, false),
	(166, 2, 'EXCEL', '구문', 'try...catch 문에서 예외 발생 여부와 상관없이 무조건 마지막에 실행되는 블록은?', '0', 'finally 블록은 필수로 실행됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["finally", "always", "then", "complete"]', 'JS,Finally', '2026-07-29 11:38:49.624271', '2026-07-29 11:38:49.624272', 157, 'JS', '구문', NULL, 35, 1, NULL, false),
	(167, 2, 'EXCEL', '구문', '자바스크립트의 비동기 처리를 유연하게 작성하도록 도와주는 객체는?', '0', 'Promise 객체가 대기, 이행, 거부 상태를 관리합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Promise", "Callback", "Thread", "Worker"]', 'JS,Promise', '2026-07-29 11:38:49.624273', '2026-07-29 11:38:49.624275', 158, 'JS', '구문', NULL, 40, 1, NULL, false),
	(168, 2, 'EXCEL', '구문', 'Promise 객체의 3가지 상태에 해당하지 않는 것은?', '3', 'Promise의 상태는 Pending, Fulfilled, Rejected 3가지입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["Pending", "Fulfilled", "Rejected", "Executing"]', 'JS,PromiseState', '2026-07-29 11:38:49.624276', '2026-07-29 11:38:49.624277', 159, 'JS', '구문', NULL, 45, 4, NULL, false),
	(169, 2, 'EXCEL', '구문', '다음 중 모듈을 내보낼 때(Export) ES6 표준 키워드는?', '0', 'ES6 모듈 표준에서는 export / import 키워드를 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["export", "module.exports", "send", "share"]', 'JS,Export', '2026-07-29 11:38:49.624278', '2026-07-29 11:38:49.62428', 160, 'JS', '구문', NULL, 30, 1, NULL, false),
	(170, 2, 'EXCEL', '자료구조', '자바스크립트 기본 Array의 특성으로 올바른 것은?', '0', '자바스크립트 배열은 동적 객체 구조입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["동적 크기를 가지며 다양한 타입의 요소를 함께 담을 수 있다.", "고정된 크기를 가진다.", "단일 타입만 허용한다.", "인덱스 접근이 불가능하다."]', 'JS,ArrayType', '2026-07-29 11:38:49.624281', '2026-07-29 11:38:49.624282', 161, 'JS', '자료구조', NULL, 35, 1, NULL, false),
	(171, 2, 'EXCEL', '자료구조', '배열의 맨 뒤에 요소를 추가하는 메서드는?', '0', 'push() 메서드가 배열 끝에 새 요소를 추가합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["push()", "pop()", "unshift()", "shift()"]', 'JS,ArrayPush', '2026-07-29 11:38:49.624283', '2026-07-29 11:38:49.624285', 162, 'JS', '자료구조', NULL, 30, 1, NULL, false),
	(172, 2, 'EXCEL', '자료구조', '배열의 맨 앞에 요소를 제거하는 메서드는?', '0', 'shift() 메서드는 첫 번째 요소를 제거하고 반환합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["shift()", "unshift()", "pop()", "splice()"]', 'JS,ArrayShift', '2026-07-29 11:38:49.624286', '2026-07-29 11:38:49.624287', 163, 'JS', '자료구조', NULL, 30, 1, NULL, false),
	(173, 2, 'EXCEL', '자료구조', '배열 요소를 순회하며 조건에 맞는 새 배열을 필터링하는 고차함수는?', '0', 'filter()는 콜백 함수가 true를 반환하는 요소로 새 배열을 만듭니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["filter()", "map()", "reduce()", "forEach()"]', 'JS,ArrayFilter', '2026-07-29 11:38:49.624288', '2026-07-29 11:38:49.62429', 164, 'JS', '자료구조', NULL, 35, 1, NULL, false),
	(174, 2, 'EXCEL', '자료구조', '배열 요소를 순회하며 각 요소를 변형한 새 배열을 만드는 고차함수는?', '0', 'map() 메서드는 요소를 변환하여 신규 배열을 반환합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["map()", "filter()", "some()", "find()"]', 'JS,ArrayMap', '2026-07-29 11:38:49.624291', '2026-07-29 11:38:49.624292', 165, 'JS', '자료구조', NULL, 35, 1, NULL, false),
	(175, 2, 'EXCEL', '자료구조', 'Set 객체의 주요 특징은?', '0', 'Set은 중복을 허용하지 않는 데이터 집합입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["중복되지 않는 유일한 값들의 집합", "키-값 쌍의 저장소", "인덱스 기반 순서 저장", "LIFO 스택 구조"]', 'JS,Set', '2026-07-29 11:38:49.624295', '2026-07-29 11:38:49.624297', 166, 'JS', '자료구조', NULL, 35, 1, NULL, false),
	(176, 2, 'EXCEL', '자료구조', 'Map 객체와 일반 Object의 차이점으로 올바른 것은?', '0', 'Map은 객체나 함수 등 모든 타입을 Key로 사용 가능합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["Map은 키 타입으로 모든 데이터 타입(객체 포함)을 사용할 수 있다.", "Object가 더 빠르다.", "Map은 순서를 보장하지 않는다.", "차이가 없다."]', 'JS,MapKey', '2026-07-29 11:38:49.624298', '2026-07-29 11:38:49.624299', 167, 'JS', '자료구조', NULL, 60, 1, NULL, false),
	(177, 2, 'EXCEL', '자료구조', 'WeakMap의 특징으로 올바른 것은?', '0', 'WeakMap의 키 객체는 참조가 사라지면 가비지 컬렉션에 의해 자동 정리됩니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["Key가 반드시 객체(Object)이어야 하며 약한 참조를 하여 가비지 컬렉션의 대상이 된다.", "문자열 Key만 가능", "요소 개수를 size로 조회 가능", "순회가 가능하다"]', 'JS,WeakMap', '2026-07-29 11:38:49.624301', '2026-07-29 11:38:49.624302', 168, 'JS', '자료구조', NULL, 70, 1, NULL, false),
	(178, 2, 'EXCEL', '자료구조', '배열의 모든 요소를 하나의 단일 값으로 축약할 때 사용하는 고차함수는?', '0', 'reduce() 메서드는 누적값을 계산하여 최종 결과 하나를 생성합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["reduce()", "concat()", "join()", "slice()"]', 'JS,Reduce', '2026-07-29 11:38:49.624304', '2026-07-29 11:38:49.624305', 169, 'JS', '자료구조', NULL, 50, 1, NULL, false),
	(179, 2, 'EXCEL', '자료구조', '기존 배열을 변경하지 않고(immutable) 특정 범위의 요소들을 복사하여 배열로 반환하는 메서드는?', '0', 'slice()는 원본을 유지하고 splice()는 원본을 변경합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["slice()", "splice()", "push()", "reverse()"]', 'JS,SliceVsSplice', '2026-07-29 11:38:49.624307', '2026-07-29 11:38:49.624308', 170, 'JS', '자료구조', NULL, 40, 1, NULL, false),
	(180, 5, 'EXCEL', 'spring 프레임워크', '스프링 프레임워크의 핵심 특징인 PoJo(Plain Old Java Object)란?', '0', 'POJO는 특정한 규약이나 클래스에 종속되지 않는 순수한 자바 객체를 뜻합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["특정 프레임워크에 종속되지 않은 순수한 자바 객체", "스프링 전용 부모 클래스를 상속받은 객체", "EJB 기반 객체", "인터페이스로만 이루어진 객체"]', 'Spring,POJO', '2026-07-29 11:38:49.624309', '2026-07-29 11:38:49.624311', 171, 'SPRING', 'spring 프레임워크', NULL, 40, 1, NULL, false),
	(181, 5, 'EXCEL', 'spring 프레임워크', '스프링의 삼대 핵심 요소에 해당하지 않는 것은?', '3', '스프링의 3대 핵심 삼각형 개념은 IoC/DI, AOP, PSA입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["IoC/DI", "AOP", "PSA (Portable Service Abstraction)", "MVC 패턴 표준화 강제"]', 'Spring,Triad', '2026-07-29 11:38:49.624312', '2026-07-29 11:38:49.624314', 172, 'SPRING', 'spring 프레임워크', NULL, 35, 4, NULL, false),
	(182, 5, 'EXCEL', 'spring 프레임워크', '스프링 부트(Spring Boot)의 대표적인 장점이 아닌 것은?', '3', '스프링 부트는 개발 생산성을 높이는 자바 설정 지원 프레임워크입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["내장 웹 서버(Tomcat 등) 제공", "Auto Configuration (자동 설정)", "의존성 라이브러리 버전 관리 (Starter)", "자바 소스 코드를 C++로 자동 변환"]', 'Spring,SpringBoot', '2026-07-29 11:38:49.624315', '2026-07-29 11:38:49.624317', 173, 'SPRING', 'spring 프레임워크', NULL, 35, 4, NULL, false),
	(183, 5, 'EXCEL', 'spring 프레임워크', 'Spring Boot 프로젝트의 메인 클래스 위에 붙이는 종합 어노테이션은?', '0', '@SpringBootApplication 어노테이션을 붙입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@SpringBootApplication", "@EnableAutoConfiguration", "@ComponentScan", "@Configuration"]', 'Spring,SpringBootApp', '2026-07-29 11:38:49.624318', '2026-07-29 11:38:49.624319', 174, 'SPRING', 'spring 프레임워크', NULL, 30, 1, NULL, false),
	(184, 5, 'EXCEL', 'spring 프레임워크', 'application.properties 또는 application.yml 파일의 용도는?', '0', '포트 번호, DB 접속 정보 등 애플리케이션 환경을 설정합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["애플리케이션 환경 설정 값 관리", "자바 클래스 정의", "HTML 템플릿 작성", "DB 테이블 생성"]', 'Spring,AppProperties', '2026-07-29 11:38:49.624321', '2026-07-29 11:38:49.624322', 175, 'SPRING', 'spring 프레임워크', NULL, 30, 1, NULL, false),
	(185, 5, 'EXCEL', 'spring 프레임워크', '스프링 프레임워크에서 객체의 생성 및 생명주기를 관리하는 주체는?', '0', 'Spring의 IoC 컨테이너가 빈의 생성 및 관리를 전담합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Spring IoC Container (ApplicationContext)", "JVM", "Web Browser", "Operating System"]', 'Spring,Container', '2026-07-29 11:38:49.624324', '2026-07-29 11:38:49.624325', 176, 'SPRING', 'spring 프레임워크', NULL, 35, 1, NULL, false),
	(186, 5, 'EXCEL', 'spring 프레임워크', '스프링이 지원하는 서비스 추상화(PSA)의 대표적인 예시는?', '0', 'PlatformTransactionManager를 통해 다양한 DB 환경을 단일 인터페이스로 추상화합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["Spring Transaction Manager (PlatformTransactionManager)", "Java Reflection", "Servlet API 직접 호출", "System.out.println"]', 'Spring,PSA', '2026-07-29 11:38:49.624327', '2026-07-29 11:38:49.624328', 177, 'SPRING', 'spring 프레임워크', NULL, 65, 1, NULL, false),
	(187, 5, 'EXCEL', 'spring 프레임워크', '스프링 프로젝트 빌드 도구로 주로 활용되는 것 2가지는?', '0', '자바 생태계에서는 Maven과 Gradle을 빌드 도구로 활용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Maven, Gradle", "npm, yarn", "pip, poetry", "make, cmake"]', 'Spring,BuildTool', '2026-07-29 11:38:49.624329', '2026-07-29 11:38:49.624331', 178, 'SPRING', 'spring 프레임워크', NULL, 30, 1, NULL, false),
	(188, 5, 'EXCEL', 'spring 프레임워크', '스프링 부트 스타터(Starter) 의존성의 역할은?', '0', 'starter 의존성은 필요한 라이브러리 그룹을 한번에 의존성 추가해줍니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["관련된 라이브러리 묶음을 간편하게 가져와버전 관리 통합 제공", "코드 자동 완성", "서버 호스팅", "데이터베이스 자동 생성"]', 'Spring,Starter', '2026-07-29 11:38:49.624332', '2026-07-29 11:38:49.624334', 179, 'SPRING', 'spring 프레임워크', NULL, 40, 1, NULL, false),
	(189, 5, 'EXCEL', 'spring 프레임워크', '스프링 빈(Bean)의 기본 스코프(Scope)는?', '0', '스프링 빈의 기본 스코프는 단 하나의 인스턴스만 공유하는 singleton입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["singleton", "prototype", "request", "session"]', 'Spring,Scope', '2026-07-29 11:38:49.624335', '2026-07-29 11:38:49.624337', 180, 'SPRING', 'spring 프레임워크', NULL, 30, 1, NULL, false),
	(190, 5, 'EXCEL', 'IOC', 'IoC (Inversion of Control, 제어의 역전)의 개념으로 올바른 것은?', '0', '제어권이 프레임워크 컨테이너로 넘어가는 현상을 제어의 역전이라 합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["객체의 생성 및 의존성 관리 주도권이 개발자에서 프레임워크로 넘어감", "개발자가 직접 new 연산자로 모든 객체를 생성 및 연결함", "C언어 형태로 포인터를 다룸", "프로그램이 제어 불가능한 상태가 됨"]', 'Spring,IoC', '2026-07-29 11:38:49.624338', '2026-07-29 11:38:49.62434', 181, 'SPRING', 'IOC', NULL, 35, 1, NULL, false),
	(191, 5, 'EXCEL', 'IOC', 'DI (Dependency Injection, 의존성 주입)의 3가지 방식 중 권장되는 방식은?', '0', '불변성(final) 보장 및 순환 참조 방지를 위해 생성자 주입이 가장 권장됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["생성자 주입 (Constructor Injection)", "필드 주입 (@Autowired Field)", "Setter 주입", "메서드 주입"]', 'Spring,DI', '2026-07-29 11:38:49.624341', '2026-07-29 11:38:49.624343', 182, 'SPRING', 'IOC', NULL, 45, 1, NULL, false),
	(192, 5, 'EXCEL', 'IOC', '스프링에서 빈(Bean)을 등록하기 위해 클래스에 붙이는 기본 어노테이션은?', '0', '@Component 및 그 파생 어노테이션(@Service, @Repository 등)을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Component", "@Inject", "@Resource", "@Bean"]', 'Spring,Component', '2026-07-29 11:38:49.624344', '2026-07-29 11:38:49.624345', 183, 'SPRING', 'IOC', NULL, 30, 1, NULL, false),
	(193, 5, 'EXCEL', 'IOC', '@Configuration 클래스 내에서 메서드 단위로 빈을 직접 등록할 때 사용하는 어노테이션은?', '0', '@Configuration 클래스의 메서드에 @Bean을 붙여 객체를 빈으로 등록합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Bean", "@Component", "@Service", "@Register"]', 'Spring,BeanAnno', '2026-07-29 11:38:49.624347', '2026-07-29 11:38:49.624348', 184, 'SPRING', 'IOC', NULL, 35, 1, NULL, false),
	(194, 5, 'EXCEL', 'IOC', '동일한 타입의 빈이 2개 이상 있을 때 특정 빈의 이름을 지정하여 주입받도록 돕는 어노테이션은?', '0', '@Qualifier("빈이름") 구문을 사용해 주입 대상을 명시합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["@Qualifier", "@Primary", "@Resource", "@Autowired"]', 'Spring,Qualifier', '2026-07-29 11:38:49.62435', '2026-07-29 11:38:49.624351', 185, 'SPRING', 'IOC', NULL, 50, 1, NULL, false),
	(195, 5, 'EXCEL', 'IOC', '동일한 타입의 빈 중 최우선적으로 주입되도록 지정하는 어노테이션은?', '0', '@Primary 어노테이션이 설정된 빈이 우선순위를 가집니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Primary", "@Qualifier", "@First", "@Main"]', 'Spring,Primary', '2026-07-29 11:38:49.624353', '2026-07-29 11:38:49.624354', 186, 'SPRING', 'IOC', NULL, 40, 1, NULL, false),
	(196, 5, 'EXCEL', 'IOC', '스프링 빈의 생명주기(Lifecycle) 콜백 메서드를 지정할 때 사용하는 자바 표준 어노테이션 2가지는?', '0', '@PostConstruct와 @PreDestroy 어노테이션을 주로 사용합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["@PostConstruct, @PreDestroy", "@Init, @Destroy", "@Before, @After", "@Start, @Stop"]', 'Spring,Lifecycle', '2026-07-29 11:38:49.624356', '2026-07-29 11:38:49.624357', 187, 'SPRING', 'IOC', NULL, 50, 1, NULL, false),
	(197, 5, 'EXCEL', 'IOC', 'ApplicationContext와 BeanFactory의 관계는?', '0', 'ApplicationContext는 BeanFactory에 메시지 다국화, 이벤트 송수신 등의 기능을 추가한 인터페이스입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["ApplicationContext가 BeanFactory를 상속받은 상위 기능의 컨테이너이다.", "BeanFactory가 상위 기능이다.", "동일한 클래스이다.", "전혀 관련이 없다."]', 'Spring,ApplicationContext', '2026-07-29 11:38:49.624359', '2026-07-29 11:38:49.62436', 188, 'SPRING', 'IOC', NULL, 50, 1, NULL, false),
	(198, 5, 'EXCEL', 'IOC', 'Lombok 라이브러리를 이용하여 생성자 주입 코드를 자동으로 만들어주는 어노테이션은?', '0', '@RequiredArgsConstructor는 final 필드에 대해 생성자를 자동 생성합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@RequiredArgsConstructor", "@AllArgsConstructor", "@NoArgsConstructor", "@Data"]', 'Spring,Lombok', '2026-07-29 11:38:49.624361', '2026-07-29 11:38:49.624363', 189, 'SPRING', 'IOC', NULL, 35, 1, NULL, false),
	(199, 5, 'EXCEL', 'IOC', '스프링 컨테이너에 의해 관리되는 자바 객체를 무엇이라고 부르는가?', '0', '스프링 컨테이너가 관리하는 객체를 빈(Bean)이라고 합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Spring Bean (스프링 빈)", "Spring Entity", "Spring DTO", "Spring Servlet"]', 'Spring,Bean', '2026-07-29 11:38:49.624364', '2026-07-29 11:38:49.624366', 190, 'SPRING', 'IOC', NULL, 25, 1, NULL, false),
	(200, 5, 'EXCEL', 'AOP', 'AOP (Aspect-Oriented Programming, 관점 지향 프로그래밍)의 핵심 목적은?', '0', '로깅, 트랜잭션, 보안 등 공통 모듈을 비즈니스 로직과 분리하는 기법입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["핵심 비즈니스 로직과 공통 관심 사항(Cross-cutting Concerns)의 분리", "객체지향 프로그래밍 대체", "DB 쿼리 자동화", "UI 디자인 개선"]', 'Spring,AOP', '2026-07-29 11:38:49.624367', '2026-07-29 11:38:49.624369', 191, 'SPRING', 'AOP', NULL, 40, 1, NULL, false),
	(201, 5, 'EXCEL', 'AOP', 'AOP 용어 중 ''공통 기능이 적용될 위치(메서드 조인포인트)''를 선정한 표현식 명칭은?', '0', 'Pointcut은 어드바이스가 적용될 조인 포인트를 필터링하는 조건식입니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["Pointcut (포인트컷)", "Advice (어드바이스)", "Aspect (애스펙트)", "Target (타겟)"]', 'Spring,Pointcut', '2026-07-29 11:38:49.62437', '2026-07-29 11:38:49.624371', 192, 'SPRING', 'AOP', NULL, 60, 1, NULL, false),
	(202, 5, 'EXCEL', 'AOP', 'AOP 용어 중 ''부가 기능을 담은 실체 모듈''을 의미하는 것은?', '0', 'Advice는 실제로 실행될 부가 기능 로직(Before, After, Around 등)입니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["Advice (어드바이스)", "Pointcut", "JoinPoint", "Weaving"]', 'Spring,Advice', '2026-07-29 11:38:49.624373', '2026-07-29 11:38:49.624374', 193, 'SPRING', 'AOP', NULL, 50, 1, NULL, false),
	(203, 5, 'EXCEL', 'AOP', 'Target 메서드 실행 전후 및 예외 발생 시까지 전체를 제어할 수 있는 가장 강력한 Advice 타입은?', '0', '@Around 어드바이스는 ProceedingJoinPoint를 통해 실행 시점을 완벽 제어합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["@Around", "@Before", "@AfterReturning", "@AfterThrowing"]', 'Spring,Around', '2026-07-29 11:38:49.624376', '2026-07-29 11:38:49.624377', 194, 'SPRING', 'AOP', NULL, 50, 1, NULL, false),
	(204, 5, 'EXCEL', 'AOP', '스프링 AOP가 내부적으로 구현되는 기본 기술 방식은?', '0', '스프링 AOP는 JDK Dynamic Proxy 및 CGLIB를 이용한 프록시 패턴으로 동작합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["동적 프록시 (Dynamic Proxy / CGLIB)", "바이트코드 직접 수정", "컴파일 타임 위빙", "JVM 수정"]', 'Spring,Proxy', '2026-07-29 11:38:49.624379', '2026-07-29 11:38:49.62438', 195, 'SPRING', 'AOP', NULL, 65, 1, NULL, false),
	(205, 5, 'EXCEL', 'AOP', 'AOP 어노테이션을 사용하기 위해 클래스에 붙이는 어노테이션은?', '0', '@Aspect 어노테이션을 통해 애스펙트 모듈임을 선언합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Aspect", "@AopClass", "@Pointcut", "@Advisor"]', 'Spring,AspectAnno', '2026-07-29 11:38:49.624381', '2026-07-29 11:38:49.624383', 196, 'SPRING', 'AOP', NULL, 35, 1, NULL, false),
	(206, 5, 'EXCEL', 'AOP', '다음 중 공통 관심 사항(Cross-cutting Concern)의 예시로 적절하지 않은 것은?', '0', '회원 가입 자체는 핵심 비즈니스 로직(Core Concern)입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["회원 가입 비즈니스 로직", "로깅 (Logging)", "트랜잭션 처리 (Transaction)", "성능 측정 (Profiling)"]', 'Spring,Concern', '2026-07-29 11:38:49.624384', '2026-07-29 11:38:49.624386', 197, 'SPRING', 'AOP', NULL, 35, 1, NULL, false),
	(207, 5, 'EXCEL', 'AOP', 'Pointcut 표현식에서 execution(* com.example.service.*.*(..)) 의 의미는?', '0', '해당 패키지 아래의 모든 메서드 실행 지점을 의미합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["com.example.service 패키지 내 모든 클래스의 모든 메서드", "특정 메서드 하나만 지정", "리턴 타입이 void인 메서드만 지정", "생성자만 지정"]', 'Spring,PointcutExpr', '2026-07-29 11:38:49.624387', '2026-07-29 11:38:49.624389', 198, 'SPRING', 'AOP', NULL, 70, 1, NULL, false),
	(208, 5, 'EXCEL', 'AOP', '어드바이스가 적용되는 위치(메서드 호출, 객체 생성 등)를 가리키는 용어는?', '0', 'Join Point는 프레임워크가 AOP를 적용할 수 있는 지점들을 의미합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["Join Point (조인 포인트)", "Aspect", "Weaving", "Target"]', 'Spring,JoinPoint', '2026-07-29 11:38:49.62439', '2026-07-29 11:38:49.624391', 199, 'SPRING', 'AOP', NULL, 50, 1, NULL, false),
	(209, 5, 'EXCEL', 'AOP', 'Aspect를 Target 객체에 적용하여 프록시 객체를 생성하는 과정을 무엇이라 하는가?', '0', '위빙(Weaving)은 포인트컷에 지정된 타겟에 애스펙트를 연결하는 과정입니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["Weaving (위빙)", "Injecting", "Linking", "Compiling"]', 'Spring,Weaving', '2026-07-29 11:38:49.624393', '2026-07-29 11:38:49.624394', 200, 'SPRING', 'AOP', NULL, 65, 1, NULL, false);
INSERT INTO public.questions (id, subject_id, question_type, title, content, correct_answer, explanation, difficulty, source_file, options, tags, created_at, updated_at, external_id, subject_code, subject_unit, code_snippet, benchmark_time, correct_option, answer_code_snippet, is_required) VALUES
	(210, 5, 'EXCEL', 'ORM', '자바의 ORM (Object-Relational Mapping) 표준 기술 명세는?', '0', 'JPA는 자바 진영의 ORM 표준 인터페이스 명세입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["JPA (Java Persistence API)", "MyBatis", "JDBC", "Hibernate"]', 'Spring,JPA', '2026-07-29 11:38:49.624396', '2026-07-29 11:38:49.624397', 201, 'SPRING', 'ORM', NULL, 30, 1, NULL, false),
	(211, 5, 'EXCEL', 'ORM', 'JPA의 대표적인 구현체(Implementation) 라이브러리는?', '0', 'Hibernate가 가장 대표적인 JPA 구현체입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Hibernate", "Spring Data", "iBatis", "QueryDSL"]', 'Spring,Hibernate', '2026-07-29 11:38:49.624399', '2026-07-29 11:38:49.6244', 202, 'SPRING', 'ORM', NULL, 30, 1, NULL, false),
	(212, 5, 'EXCEL', 'ORM', '데이터베이스 테이블과 매핑되는 자바 클래스 위에 붙이는 필수 어노테이션은?', '0', '@Entity 어노테이션을 통해 JPA 매핑 대상임을 나타냅니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Entity", "@Table", "@Column", "@Model"]', 'Spring,Entity', '2026-07-29 11:38:49.624402', '2026-07-29 11:38:49.624403', 203, 'SPRING', 'ORM', NULL, 30, 1, NULL, false),
	(213, 5, 'EXCEL', 'ORM', '엔티티의 기본키(Primary Key)를 지정할 때 사용하는 어노테이션은?', '0', '@Id 어노테이션을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Id", "@Key", "@PrimaryKey", "@GeneratedValue"]', 'Spring,Id', '2026-07-29 11:38:49.624404', '2026-07-29 11:38:49.624406', 204, 'SPRING', 'ORM', NULL, 25, 1, NULL, false),
	(214, 5, 'EXCEL', 'ORM', 'Spring Data JPA에서 기본 CRUD 메서드를 제공받기 위해 상속받는 인터페이스는?', '0', 'JpaRepository<Entity, IdType> 인터페이스를 상속합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["JpaRepository<T, ID>", "CrudInterface", "OrmRepository", "BaseMapper"]', 'Spring,JpaRepository', '2026-07-29 11:38:49.624407', '2026-07-29 11:38:49.624409', 205, 'SPRING', 'ORM', NULL, 35, 1, NULL, false),
	(215, 5, 'EXCEL', 'ORM', 'JPA의 영속성 컨텍스트(Persistence Context)가 제공하는 이점이 아닌 것은?', '3', '서버 자동 증설은 인프라 영역이며 영속성 컨텍스트의 이점이 아닙니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["1차 캐시 보장", "동일성(Identity) 보장", "쓰기 지연 (Transactional Write-Behind)", "DB 물리적 서버 자동 증설"]', 'Spring,PersistenceContext', '2026-07-29 11:38:49.62441', '2026-07-29 11:38:49.624412', 206, 'SPRING', 'ORM', NULL, 70, 4, NULL, false),
	(216, 5, 'EXCEL', 'ORM', 'N+1 문제의 발생 원인과 해결 방법으로 가장 올바른 조합은?', '0', '연관관계 조회 시 발생하며 Fetch Join 구문으로 한 번에 조인 조회하여 해결합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["하위 엔티티 조회 시 N번의 쿼리 추가 발생 / Fetch Join 또는 @EntityGraph 사용", "DB 락 문제 / 트랜잭션 롤백", "메모리 부족 / 캐시 삭제", "PK 중복 / ID 자동증가"]', 'Spring,NPlusOne', '2026-07-29 11:38:49.624413', '2026-07-29 11:38:49.624414', 207, 'SPRING', 'ORM', NULL, 75, 1, NULL, false),
	(217, 5, 'EXCEL', 'ORM', 'JPA에서 엔티티의 상태 변화(INSERT/UPDATE/DELETE)를 DB에 실제 반영하는 메서드는?', '0', 'flush() 메서드는 영속성 컨텍스트의 변경 내용을 데이터베이스에 동기화합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["em.flush()", "em.persist()", "em.clear()", "em.detach()"]', 'Spring,Flush', '2026-07-29 11:38:49.624416', '2026-07-29 11:38:49.624417', 208, 'SPRING', 'ORM', NULL, 50, 1, NULL, false),
	(218, 5, 'EXCEL', 'ORM', 'Spring Data JPA에서 메서드 이름만으로 쿼리를 자동 생성하는 기능 명칭은?', '0', 'findByUsernameAndAge처럼 메서드 명명 규칙으로 쿼리를 만듭니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["쿼리 메서드 (Query Method)", "JPQL", "Native Query", "Criteria"]', 'Spring,QueryMethod', '2026-07-29 11:38:49.624419', '2026-07-29 11:38:49.62442', 209, 'SPRING', 'ORM', NULL, 40, 1, NULL, false),
	(219, 5, 'EXCEL', 'ORM', 'JPA 연관관계 매핑 중 1:N 관계를 표현할 때 사용하는 어노테이션은?', '0', '@OneToMany 어노테이션을 매핑합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@OneToMany", "@ManyToOne", "@OneToOne", "@ManyToMany"]', 'Spring,OneToMany', '2026-07-29 11:38:49.624421', '2026-07-29 11:38:49.624423', 210, 'SPRING', 'ORM', NULL, 30, 1, NULL, false),
	(220, 5, 'EXCEL', 'Annotation', '스프링 MVC에서 해당 클래스가 웹 요청을 처리하는 컨트롤러임을 나타내는 어노테이션은?', '0', '@Controller 어노테이션을 지정합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Controller", "@Service", "@Repository", "@Component"]', 'Spring,Controller', '2026-07-29 11:38:49.624424', '2026-07-29 11:38:49.624427', 211, 'SPRING', 'Annotation', NULL, 30, 1, NULL, false),
	(221, 5, 'EXCEL', 'Annotation', 'RESTful 웹 서비스를 제공하며 JSON 형태로 응답을 직접 반환하는 컨트롤러 어노테이션은?', '0', '@RestController는 @Controller + @ResponseBody 기능이 합쳐진 것입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@RestController", "@Controller", "@ResponseBodyController", "@WebController"]', 'Spring,RestController', '2026-07-29 11:38:49.624428', '2026-07-29 11:38:49.624429', 212, 'SPRING', 'Annotation', NULL, 30, 1, NULL, false),
	(222, 5, 'EXCEL', 'Annotation', '클라이언트의 HTTP GET 요청을 처리할 메서드에 붙이는 어노테이션은?', '0', '@GetMapping("/url") 구문을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@GetMapping", "@PostMapping", "@PutMapping", "@DeleteMapping"]', 'Spring,GetMapping', '2026-07-29 11:38:49.624431', '2026-07-29 11:38:49.624432', 213, 'SPRING', 'Annotation', NULL, 25, 1, NULL, false),
	(223, 5, 'EXCEL', 'Annotation', 'URL 경로에 포함된 변수(예: /users/{id})의 값을 파라미터로 추출하는 어노테이션은?', '0', '@PathVariable("id") 어노테이션을 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@PathVariable", "@RequestParam", "@RequestBody", "@ModelAttribute"]', 'Spring,PathVariable', '2026-07-29 11:38:49.624433', '2026-07-29 11:38:49.624434', 214, 'SPRING', 'Annotation', NULL, 35, 1, NULL, false),
	(224, 5, 'EXCEL', 'Annotation', 'HTTP 요청의 Body에 담긴 JSON 데이터를 자바 객체로 변환받는 어노테이션은?', '0', '@RequestBody가 JSON을 Jackson 라이브러리를 통해 자바 DTO로 변환합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@RequestBody", "@ResponseBody", "@RequestParam", "@ModelAttribute"]', 'Spring,RequestBody', '2026-07-29 11:38:49.624436', '2026-07-29 11:38:49.624437', 215, 'SPRING', 'Annotation', NULL, 35, 1, NULL, false),
	(225, 5, 'EXCEL', 'Annotation', 'HTTP 요청 파라미터(쿼리 스트링 또는 Form 데이터)를 전달받을 때 사용하는 어노테이션은?', '0', '@RequestParam("name") 형태를 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@RequestParam", "@RequestBody", "@PathVariable", "@Header"]', 'Spring,RequestParam', '2026-07-29 11:38:49.624438', '2026-07-29 11:38:49.624439', 216, 'SPRING', 'Annotation', NULL, 35, 1, NULL, false),
	(226, 5, 'EXCEL', 'Annotation', '선언적 트랜잭션 처리를 위해 서비스 메서드 또는 클래스 위에 붙이는 어노테이션은?', '0', '@Transactional 어노테이션을 부여합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Transactional", "@EnableTransaction", "@Tx", "@Commit"]', 'Spring,Transactional', '2026-07-29 11:38:49.624441', '2026-07-29 11:38:49.624442', 217, 'SPRING', 'Annotation', NULL, 30, 1, NULL, false),
	(227, 5, 'EXCEL', 'Annotation', '스프링의 서비스 계층(Business Logic) 비즈니스 모듈에 붙이는 어노테이션은?', '0', '@Service 어노테이션을 붙여 명시합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Service", "@Repository", "@Controller", "@Component"]', 'Spring,Service', '2026-07-29 11:38:49.624443', '2026-07-29 11:38:49.624444', 218, 'SPRING', 'Annotation', NULL, 25, 1, NULL, false),
	(228, 5, 'EXCEL', 'Annotation', '데이터 Access 계층(DAO 또는 Repository) 클래스에 붙이는 어노테이션은?', '0', '@Repository 어노테이션을 붙이며 DB 예외 추상화 변환을 지원합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Repository", "@Service", "@Controller", "@Data"]', 'Spring,Repository', '2026-07-29 11:38:49.624446', '2026-07-29 11:38:49.624447', 219, 'SPRING', 'Annotation', NULL, 25, 1, NULL, false),
	(229, 5, 'EXCEL', 'Annotation', '스프링 환경에서 외부 설정 파일의 값을 자바 변수에 주입받을 때 쓰는 어노테이션은?', '0', '@Value 어노테이션을 사용하여 application.yml 속성을 주입받습니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["@Value(\"${property.key}\")", "@Property", "@Config", "@Inject"]', 'Spring,Value', '2026-07-29 11:38:49.624448', '2026-07-29 11:38:49.62445', 220, 'SPRING', 'Annotation', NULL, 45, 1, NULL, false),
	(230, 5, 'EXCEL', 'security', 'Spring Security의 기본 동작 원리 메커니즘은?', '0', 'Spring Security는 DelegatingFilterProxy 기반의 필터 체인으로 구동됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["서블릿 필터 체인 (Servlet Filter Chain)", "AOP 위빙", "인터셉터 (HandlerInterceptor)", "DB 트리거"]', 'Spring,SecurityFilter', '2026-07-29 11:38:49.624451', '2026-07-29 11:38:49.624452', 221, 'SPRING', 'security', NULL, 50, 1, NULL, false),
	(231, 5, 'EXCEL', 'security', '사용자의 신원(아이디/비밀번호)을 확인하는 과정을 무엇이라 하는가?', '0', '신원을 확인하는 과정을 인증(Authentication)이라 합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["인증 (Authentication)", "인가 (Authorization)", "암호화 (Encryption)", "세션 만료"]', 'Spring,Authentication', '2026-07-29 11:38:49.624454', '2026-07-29 11:38:49.624455', 222, 'SPRING', 'security', NULL, 30, 1, NULL, false),
	(232, 5, 'EXCEL', 'security', '인증된 사용자가 특정 리소스에 접근할 권한이 있는지 확인하는 과정은?', '0', '권한 유무를 검증하는 단계를 인가(Authorization)라 합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["인가 (Authorization)", "인증 (Authentication)", "토큰 발행", "해싱"]', 'Spring,Authorization', '2026-07-29 11:38:49.624457', '2026-07-29 11:38:49.624459', 223, 'SPRING', 'security', NULL, 30, 1, NULL, false),
	(233, 5, 'EXCEL', 'security', '사용자 정보를 DB에서 조회하여 UserDetails 객체로 반환하는 커스텀 서비스 인터페이스는?', '0', 'UserDetailsService의 loadUserByUsername() 메서드를 구현해야 합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["UserDetailsService", "AuthenticationProvider", "SecurityContextHolder", "PasswordEncoder"]', 'Spring,UserDetailsService', '2026-07-29 11:38:49.62446', '2026-07-29 11:38:49.624462', 224, 'SPRING', 'security', NULL, 55, 1, NULL, false),
	(234, 5, 'EXCEL', 'security', '비밀번호를 안전하게 단방향 해시 암호화하기 위해 스프링 세큐리티가 제공하는 표준 암호화 클래스는?', '0', 'BCryptPasswordEncoder가 표준으로 가장 널리 권장됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["BCryptPasswordEncoder", "MD5PasswordEncoder", "SHA1Encoder", "PlainTextEncoder"]', 'Spring,BCrypt', '2026-07-29 11:38:49.624463', '2026-07-29 11:38:49.624465', 225, 'SPRING', 'security', NULL, 35, 1, NULL, false),
	(235, 5, 'EXCEL', 'security', '웹 애플리케이션 보안 공격 중 사이트 간 요청 위조 공격 방어를 나타내는 키워드는?', '0', 'CSRF 방어 토큰을 생성하여 비인가 요청을 차단합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CSRF (Cross-Site Request Forgery)", "XSS", "SQL Injection", "CORS"]', 'Spring,CSRF', '2026-07-29 11:38:49.624466', '2026-07-29 11:38:49.624467', 226, 'SPRING', 'security', NULL, 40, 1, NULL, false),
	(236, 5, 'EXCEL', 'security', '현재 인증된 사용자의 보안 컨텍스트(Authentication 객체)가 저장되는 공간은?', '0', 'SecurityContextHolder -> SecurityContext -> Authentication 구조로 저장됩니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["SecurityContextHolder", "HttpSession", "ServletConfig", "ApplicationContext"]', 'Spring,SecurityContext', '2026-07-29 11:38:49.624469', '2026-07-29 11:38:49.62447', 227, 'SPRING', 'security', NULL, 65, 1, NULL, false),
	(237, 5, 'EXCEL', 'security', 'REST API 환경에서 무상태(Stateless) 인증을 위해 가장 흔히 쓰이는 토큰 방식은?', '0', 'JWT 토큰을 사용하여 세션 없이 인증 상태를 처리합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["JWT (JSON Web Token)", "JSESSIONID", "Cookie", "OAuth1"]', 'Spring,JWT', '2026-07-29 11:38:49.624471', '2026-07-29 11:38:49.624473', 228, 'SPRING', 'security', NULL, 30, 1, NULL, false),
	(238, 5, 'EXCEL', 'security', '다른 출처(Origin)의 리소스 요청을 허용/제한하는 웹 보안 정책은?', '0', 'CORS 설정을 통해 프론트엔드 도메인의 접근을 허용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["CORS (Cross-Origin Resource Sharing)", "CSRF", "XSS", "SSRF"]', 'Spring,CORS', '2026-07-29 11:38:49.624474', '2026-07-29 11:38:49.624475', 229, 'SPRING', 'security', NULL, 35, 1, NULL, false),
	(239, 5, 'EXCEL', 'security', 'Spring Security 설정 클래스를 정의할 때 등록하는 보안 필터 체인 빈 타입은?', '0', '@Bean SecurityFilterChain filterChain(HttpSecurity http) 형태로 빈을 정의합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["SecurityFilterChain", "WebSecurityConfigurer", "AuthenticationManager", "FilterManager"]', 'Spring,SecurityFilterChain', '2026-07-29 11:38:49.624477', '2026-07-29 11:38:49.624478', 230, 'SPRING', 'security', NULL, 55, 1, NULL, false),
	(240, 5, 'EXCEL', 'restAPI', 'REST (Representational State Transfer)의 기본 구성 요소 3가지에 해당하지 않는 것은?', '3', 'REST는 HTTP 프로토콜 표준 자원, 행위, 표현으로 구성됩니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["자원 (Resource - URI)", "행위 (Verb - HTTP Method)", "표현 (Representation - JSON/XML)", "프로토콜 (Protocol - TCP/IP 직접 연결)"]', 'Spring,REST', '2026-07-29 11:38:49.624479', '2026-07-29 11:38:49.624481', 231, 'SPRING', 'restAPI', NULL, 50, 4, NULL, false),
	(241, 5, 'EXCEL', 'restAPI', '리소스를 생성(Create)할 때 사용하는 HTTP Method는?', '0', 'POST 메서드가 생성 요청에 활용됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["POST", "GET", "PUT", "DELETE"]', 'Spring,HttpPost', '2026-07-29 11:38:49.624482', '2026-07-29 11:38:49.624483', 232, 'SPRING', 'restAPI', NULL, 25, 1, NULL, false),
	(242, 5, 'EXCEL', 'restAPI', '리소스를 수정/교체(Update)할 때 사용하는 HTTP Method는?', '0', '전체 수정은 PUT, 부분 수정은 PATCH를 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["PUT / PATCH", "GET", "POST", "OPTION"]', 'Spring,HttpPut', '2026-07-29 11:38:49.624485', '2026-07-29 11:38:49.624486', 233, 'SPRING', 'restAPI', NULL, 25, 1, NULL, false),
	(243, 5, 'EXCEL', 'restAPI', 'REST API 응답 성공 시 반환하는 대표적인 HTTP Status Code는?', '0', '200 OK 및 201 Created 가 성공 상태 코드입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["200 OK (또는 201 Created)", "400 Bad Request", "404 Not Found", "500 Server Error"]', 'Spring,Status200', '2026-07-29 11:38:49.624487', '2026-07-29 11:38:49.624488', 234, 'SPRING', 'restAPI', NULL, 25, 1, NULL, false),
	(244, 5, 'EXCEL', 'restAPI', '요청한 리소스를 찾을 수 없을 때 반환하는 HTTP Status Code는?', '0', '404 Not Found 상태 코드입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["404 Not Found", "401 Unauthorized", "403 Forbidden", "500 Internal Error"]', 'Spring,Status404', '2026-07-29 11:38:49.62449', '2026-07-29 11:38:49.624491', 235, 'SPRING', 'restAPI', NULL, 25, 1, NULL, false),
	(245, 5, 'EXCEL', 'restAPI', '인증되지 않은 사용자의 접근 시 반환하는 HTTP Status Code는?', '0', '401 Unauthorized가 인증 실패 상태 코드입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["401 Unauthorized", "403 Forbidden", "400 Bad Request", "502 Bad Gateway"]', 'Spring,Status401', '2026-07-29 11:38:49.624493', '2026-07-29 11:38:49.624494', 236, 'SPRING', 'restAPI', NULL, 30, 1, NULL, false),
	(246, 5, 'EXCEL', 'restAPI', '스프링에서 REST 응답 데이터와 HTTP 헤더, 상태코드를 모두 포함하여 반환할 수 있는 객체는?', '0', 'ResponseEntity.ok().body(data) 구조로 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["ResponseEntity<T>", "HttpEntity<T>", "RestResponse", "ModelAndView"]', 'Spring,ResponseEntity', '2026-07-29 11:38:49.624495', '2026-07-29 11:38:49.624497', 237, 'SPRING', 'restAPI', NULL, 35, 1, NULL, false),
	(247, 5, 'EXCEL', 'restAPI', '스프링 부트에서 JSON 직렬화/역직렬화를 담당하는 기본 라이브러리는?', '0', 'Jackson 라이브러리가 기본 내장되어 있습니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["Jackson", "Gson", "FastJson", "SimpleJson"]', 'Spring,Jackson', '2026-07-29 11:38:49.624498', '2026-07-29 11:38:49.624499', 238, 'SPRING', 'restAPI', NULL, 45, 1, NULL, false),
	(248, 5, 'EXCEL', 'restAPI', 'REST API 명세서를 자동 생성 및 시각화해주는 대표적인 도구는?', '0', 'Swagger/Springdoc을 통해 API 테스트 및 문서를 자동화합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Swagger (Springdoc OpenAPI)", "Postman", "JUnit", "JProfiler"]', 'Spring,Swagger', '2026-07-29 11:38:49.624501', '2026-07-29 11:38:49.624502', 239, 'SPRING', 'restAPI', NULL, 35, 1, NULL, false),
	(249, 5, 'EXCEL', 'restAPI', 'REST API 설계 가이드라인으로 올바르지 않은 것은?', '3', 'URI 마지막에는 슬래시(/)를 포함하지 않는 것이 명세 규칙입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["URI에 동사보다는 명사를 사용한다.", "자원에 대한 행위는 HTTP Method로 표현한다.", "슬래시(/)는 계층 관계를 나타낸다.", "URI 마지막에 슬래시(/)를 반드시 포함한다."]', 'Spring,RestRule', '2026-07-29 11:38:49.624504', '2026-07-29 11:38:49.624505', 240, 'SPRING', 'restAPI', NULL, 35, 4, NULL, false),
	(250, 5, 'EXCEL', 'MVC', 'Spring MVC 패턴의 3가지 구성 요소에 해당하지 않는 것은?', '3', 'MVC 패턴 기본 구성요소는 Model, View, Controller 3가지입니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Model", "View", "Controller", "Service"]', 'Spring,MVC', '2026-07-29 11:38:49.624506', '2026-07-29 11:38:49.624508', 241, 'SPRING', 'MVC', NULL, 25, 4, NULL, false),
	(251, 5, 'EXCEL', 'MVC', 'Spring MVC 프론트 컨트롤러 패턴의 핵심 클래스는?', '0', 'DispatcherServlet이 모든 중앙 HTTP 요청을 받아 적절한 컨트롤러로 위임합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["DispatcherServlet", "FilterConfig", "HttpServlet", "AppServlet"]', 'Spring,DispatcherServlet', '2026-07-29 11:38:49.624509', '2026-07-29 11:38:49.62451', 242, 'SPRING', 'MVC', NULL, 60, 1, NULL, false),
	(252, 5, 'EXCEL', 'MVC', '컨트롤러가 반환한 뷰 이름(View Name)을 바탕으로 실제 HTML/JSP 템플릿을 찾아 연결해주는 컴포넌트는?', '0', 'ViewResolver가 뷰 이름 앞뒤로 접두사/접미사를 붙여 실제 템플릿을 찾습니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["ViewResolver", "HandlerMapping", "HandlerAdapter", "MessageConverter"]', 'Spring,ViewResolver', '2026-07-29 11:38:49.624512', '2026-07-29 11:38:49.624513', 243, 'SPRING', 'MVC', NULL, 50, 1, NULL, false),
	(253, 5, 'EXCEL', 'MVC', '클라이언트 요청 URL을 분석하여 담당 컨트롤러 메서드를 찾아주는 컴포넌트는?', '0', 'HandlerMapping 컴포넌트가 담당 컨트롤러를 매핑해줍니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["HandlerMapping", "ViewResolver", "DispatcherServlet", "Filter"]', 'Spring,HandlerMapping', '2026-07-29 11:38:49.624514', '2026-07-29 11:38:49.624516', 244, 'SPRING', 'MVC', NULL, 50, 1, NULL, false),
	(254, 5, 'EXCEL', 'MVC', 'Model 객체의 주요 역할은?', '0', 'Model 객체는 View에 전달할 데이터를 key-value로 담아 넘겨줍니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["컨트롤러에서 처리한 결과 데이터를 View로 전달하기 위한 데이터 담는 상자", "데이터베이스 테이블 정의", "HTTP 헤더 설정", "보안 필터링"]', 'Spring,Model', '2026-07-29 11:38:49.624517', '2026-07-29 11:38:49.624519', 245, 'SPRING', 'MVC', NULL, 30, 1, NULL, false),
	(255, 5, 'EXCEL', 'MVC', 'Spring Boot에서 권장하는 대표적인 서버 사이드 템플릿 엔진은?', '0', '스프링 부트에서는 Thymeleaf가 표준 템플릿 엔진으로 권장됩니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["Thymeleaf", "JSP", "Velocity", "PHP"]', 'Spring,Thymeleaf', '2026-07-29 11:38:49.62452', '2026-07-29 11:38:49.624521', 246, 'SPRING', 'MVC', NULL, 30, 1, NULL, false),
	(256, 5, 'EXCEL', 'MVC', '컨트롤러에서 데이터와 뷰 이름을 동시에 반환할 때 사용하는 스프링 클래스는?', '0', 'ModelAndView 객체에 모델 데이터와 뷰 경로를 동시에 설정하여 반환 가능합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["ModelAndView", "ModelMap", "ViewData", "DataContainer"]', 'Spring,ModelAndView', '2026-07-29 11:38:49.624523', '2026-07-29 11:38:49.624524', 247, 'SPRING', 'MVC', NULL, 35, 1, NULL, false),
	(257, 5, 'EXCEL', 'MVC', 'Spring MVC에서 인터셉터(HandlerInterceptor)가 구동되는 시점이 아닌 것은?', '3', '인터셉터는 DispatcherServlet 내부에서 구동되므로 서블릿 필터 실행 이후 동작합니다.', 'HARD', '문제은행_샘플데이터_250문항_1.xlsx', '["preHandle (컨트롤러 실행 전)", "postHandle (컨트롤러 실행 후)", "afterCompletion (뷰 렌더링 완료 후)", "beforeFilter (서블릿 필터 실행 전)"]', 'Spring,Interceptor', '2026-07-29 11:38:49.624525', '2026-07-29 11:38:49.624527', 248, 'SPRING', 'MVC', NULL, 65, 4, NULL, false),
	(258, 5, 'EXCEL', 'MVC', 'HTML Form 태그 제출 시 클라이언트 데이터의 유효성을 검증하기 위해 사용하는 어노테이션은?', '0', '@Valid 어노테이션과 Hibernate Validator 제약조건(@NotNull 등)을 조합하여 사용합니다.', 'EASY', '문제은행_샘플데이터_250문항_1.xlsx', '["@Valid (또는 @Validated)", "@Check", "@Verify", "@Test"]', 'Spring,Valid', '2026-07-29 11:38:49.624528', '2026-07-29 11:38:49.624529', 249, 'SPRING', 'MVC', NULL, 35, 1, NULL, false),
	(259, 5, 'EXCEL', 'MVC', 'Validation 검증 결과 에러 정보를 담아 컨트롤러로 전달되는 객체는?', '0', '@Valid 뒤에 BindingResult 파라미터를 선언하여 에러 내역을 확인합니다.', 'MEDIUM', '문제은행_샘플데이터_250문항_1.xlsx', '["BindingResult", "ErrorMap", "ResultStatus", "ValidationError"]', 'Spring,BindingResult', '2026-07-29 11:38:49.624531', '2026-07-29 11:38:49.624532', 250, 'SPRING', 'MVC', NULL, 45, 1, NULL, false),
	(260, 1, 'EXCEL', 'Python 기초 - 기본 개념 1', '파이썬에서 함수를 정의할 때 사용하는 예약어(Keyword)는 무엇인가요?', NULL, '파이썬에서 함수를 정의할 때 사용하는 예약어(Keyword)는 def 입니다.', 'EASY', NULL, NULL, NULL, '2026-07-31 07:19:57.461798', '2026-07-31 07:19:57.46181', NULL, NULL, NULL, NULL, NULL, NULL, 'def', false),
	(261, 1, 'EXCEL', 'Python 기초 - 기본 개념 1', '리스트(List)의 가장 마지막에 새로운 요소를 추가하고 싶을 때 사용하는 리스트 메서드는 무엇인가요?', NULL, '리스트(List)의 가장 마지막에 새로운 요소를 추가하고 싶을 때 사용하는 리스트 메서드 append()', 'EASY', NULL, NULL, NULL, '2026-07-31 07:28:49.934525', '2026-07-31 07:28:49.934543', NULL, NULL, NULL, NULL, NULL, NULL, 'append()', false),
	(262, 4, 'EXCEL', 'java 코드 짜기', '정수 2개와 연산자 1개를 입력받아 두 정수의 연산의 결과를 출력
	ex) 2 3 + => 2 + 3 = 5
	ex) 2 3 - => 2 - 3 = -1
	ex) 2 3 ! => 잘못된 연산자
 연산자는 + - * / % 5개만 가능		
 연산은 0으로 나눌때 exception 발생
 피연산자가 0이면 0으로 나눌 수 없습니다. 출력
', NULL, '', 'EASY', NULL, NULL, NULL, '2026-07-31 07:34:12.872329', '2026-07-31 07:34:12.872344', NULL, NULL, NULL, NULL, NULL, NULL, 'package day04;

import java.util.Scanner;

public class Exam01 {

	public static void main(String[] args) {
		
		Scanner scan = new Scanner(System.in);
		
		System.out.println("정수 2개와 연산자를 순서대로 입력> (2 3 +)");
		int num1 = scan.nextInt();
		int num2 = scan.nextInt();
		String op = scan.next();  
		 	
		switch(op) {
		case "+": 
			System.out.println(num1+op+num2+"="+(num1+num2));
			break;
		case "-": 
			System.out.println(num1+op+num2+"="+(num1-num2));
			break;
		case "*": 
			System.out.println(num1+op+num2+"="+(num1*num2));
			break;
		case "/": 
			if(num2 == 0) {
				System.out.println("0으로 나눌 수 없습니다.");
			}else {
				System.out.println(num1+op+num2+"="+(num1/num2));				
			}
			break;
		case "%": 
			if(num2 == 0) {
				System.out.println("0으로 나눌 수 없습니다.");
			}else {
				System.out.println(num1+op+num2+"="+(num1%num2));				
			}
			break;
		default: System.out.println("잘못된 연산자");
		}
		
		System.out.println("---------------------");
		// 미리 안되는 케이스를 빼기
		int result = 0;
		if((op.equals("/") || op.equals("%")) && num2 == 0){
			System.out.println("0으로 나눌 수 없습니다.");
			return;
		}
		
		switch(op) {
		case "+": result = num1 + num2; break;
		case "-": result = num1 - num2; break;
		case "*": result = num1 * num2; break;
		case "/": result = num1 / num2; break;
		case "%": result = num1 % num2; break;
		default: System.out.println("잘못된 연산자");
		}
		
		if(op.equals("+") || op.equals("-") || op.equals("*") || op.equals("/") || op.equals("%")) {
			System.out.println(num1+op+num2+"="+result);		
		}
		
		scan.close();
		
	}

}', false),
	(263, 1, 'EXCEL', '기본구문(조건문, 반복문)', '1~10까지 합을 출력하는 코드를 python으로 코딩하시오.', NULL, 'range(1, 11)은 1부터 10까지의 정수를 차례대로 생성합니다. 반복문에서 각 값을 total에 누적한 뒤 출력하면 결과는 55입니다.', 'EASY', NULL, NULL, NULL, '2026-07-31 08:43:31.908323', '2026-07-31 08:43:42.374329', NULL, NULL, NULL, NULL, NULL, NULL, 'total = 0

for i in range(1, 11):
    total += i

print(total)', false),
	(266, 4, 'CODE', '페이지네이션 값 계산', 'pgvo.getPageNo()가 7, pgvo.getQty()가 10, totalCount가 95일 때 생성된 PagingHandler의 startPage, endPage, prev, next 값으로 올바른 것은 무엇인가?', '0', '계산된 endPage는 ceil(7 / 10.0) × 10 = 10이고 startPage는 10 - 9 = 1이다. realEndPage는 ceil(95 / 10.0) = 10이다. startPage가 1보다 크지 않으므로 prev는 false이고, endPage가 realEndPage보다 작지 않으므로 next도 false이다.', 'MEDIUM', 'PagingHandler.java', '["startPage=1, endPage=10, prev=false, next=false", "startPage=1, endPage=9, prev=false, next=true", "startPage=7, endPage=10, prev=true, next=false", "startPage=1, endPage=10, prev=false, next=true"]', 'java', '2026-08-02 11:22:18.07938', '2026-08-02 11:22:18.079396', NULL, NULL, NULL, NULL, NULL, NULL, NULL, false),
	(267, 4, 'CODE', '이전 및 다음 페이지 그룹 존재 여부', 'pgvo.getPageNo()가 13, pgvo.getQty()가 10, totalCount가 235일 때 prev와 next의 값은 무엇인가?', '3', 'endPage는 ceil(13 / 10.0) × 10 = 20이고 startPage는 11이다. realEndPage는 ceil(235 / 10.0) = 24이다. startPage가 1보다 크므로 prev는 true이며, endPage 20이 realEndPage 24보다 작으므로 next도 true이다.', 'MEDIUM', 'PagingHandler.java', '["prev=false, next=false", "prev=false, next=true", "prev=true, next=false", "prev=true, next=true"]', 'java', '2026-08-02 11:22:18.079406', '2026-08-02 11:22:18.079414', NULL, NULL, NULL, NULL, NULL, NULL, NULL, false),
	(268, 4, 'CODE', '실수 나눗셈을 사용하는 이유', '코드에서 pgvo.getPageNo() / (pgvo.getQty() * 1.0) 및 totalCount * 1.0과 같이 1.0을 곱하는 주된 이유는 무엇인가?', '1', '두 피연산자가 모두 int이면 Java는 정수 나눗셈을 수행하여 소수 부분을 버린다. 1.0을 곱하면 피연산자가 double로 변환되므로 실수 나눗셈이 수행되고, Math.ceil()이 올림 계산을 정확히 할 수 있다.', 'EASY', 'PagingHandler.java', '["\ubaa8\ub4e0 \uacc4\uc0b0 \uacb0\uacfc\ub97c int \ud0c0\uc785\uc73c\ub85c \uac15\uc81c \ubcc0\ud658\ud558\uae30 \uc704\ud574\uc11c", "\uc815\uc218 \ub098\ub217\uc148\uc73c\ub85c \uc18c\uc218 \ubd80\ubd84\uc774 \ubc84\ub824\uc9c0\ub294 \uac83\uc744 \ub9c9\uace0 \uc2e4\uc218 \ub098\ub217\uc148\uc744 \uc218\ud589\ud558\uae30 \uc704\ud574\uc11c", "Math.ceil()\uc758 \ubc18\ud658 \ud0c0\uc785\uc744 int\ub85c \ubcc0\uacbd\ud558\uae30 \uc704\ud574\uc11c", "0\uc73c\ub85c \ub098\ub204\ub294 \uc608\uc678\ub97c \ubc29\uc9c0\ud558\uae30 \uc704\ud574\uc11c"]', 'java', '2026-08-02 11:22:18.079422', '2026-08-02 11:22:18.079429', NULL, NULL, NULL, NULL, NULL, NULL, NULL, false),
	(269, 4, 'CODE', '페이지 표시 개수 변경 시 발생하는 문제', 'pgvo.getQty()가 20, pgvo.getPageNo()가 21이고 totalCount가 1000일 때 startPage와 endPage는 무엇인가? 또한 이 결과가 보여주는 코드상의 문제는 무엇인가?', '1', 'endPage는 ceil(21 / 20.0) × 20 = 40이고 startPage는 endPage - 9이므로 31이다. endPage 계산은 qty를 페이지 그룹 크기처럼 사용하지만 startPage 계산에서는 9가 고정되어 있다. 따라서 qty가 10이 아닐 경우 계산 기준이 일치하지 않는다. 일반화하려면 startPage를 endPage - (페이지 그룹 크기 - 1) 형태로 계산해야 한다.', 'HARD', 'PagingHandler.java', '["startPage=21, endPage=40\uc774\uba70 \ubb38\uc81c\uc5c6\uc774 20\uac1c\uc758 \ud398\uc774\uc9c0 \ubc88\ud638\ub97c \ud45c\uc2dc\ud55c\ub2e4.", "startPage=31, endPage=40\uc774\uba70 startPage \uacc4\uc0b0\uc5d0 9\uac00 \uace0\uc815\ub418\uc5b4 \uc788\uc5b4 10\uac1c\uc758 \ud398\uc774\uc9c0 \ubc88\ud638\ub9cc \ud45c\uc2dc\ud55c\ub2e4.", "startPage=11, endPage=30\uc774\uba70 \ud398\uc774\uc9c0 \uadf8\ub8f9\uc774 \ud55c \uce78 \uc55e\uc73c\ub85c \uc774\ub3d9\ud55c\ub2e4.", "startPage=20, endPage=40\uc774\uba70 \ucd1d 21\uac1c\uc758 \ud398\uc774\uc9c0 \ubc88\ud638\ub97c \ud45c\uc2dc\ud55c\ub2e4."]', 'java', '2026-08-02 11:22:18.079438', '2026-08-02 11:22:18.079445', NULL, NULL, NULL, NULL, NULL, NULL, NULL, false),
	(270, 4, 'CODE', 'Setter 호출과 파생 값의 일관성', 'PagingHandler 객체를 생성한 후 setTotalCount() 또는 setPgvo()를 호출했을 때 startPage, endPage, prev, next에는 어떤 일이 발생하는가?', '2', '각 setter는 해당 필드에 새 값을 대입할 뿐 페이지네이션 계산 로직을 다시 실행하지 않는다. 따라서 totalCount나 pgvo를 변경하면 기존 startPage, endPage, prev, next가 새 데이터와 일치하지 않을 수 있다. 일관성을 유지하려면 setter에서 재계산 메서드를 호출하거나 객체를 불변으로 설계하는 방법을 고려할 수 있다.', 'HARD', 'PagingHandler.java', '["\uac01 setter\uac00 \uc0dd\uc131\uc790\ub97c \ub2e4\uc2dc \ud638\ucd9c\ud558\uc5ec \ubaa8\ub4e0 \uac12\uc774 \uc790\ub3d9\uc73c\ub85c \uc7ac\uacc4\uc0b0\ub41c\ub2e4.", "startPage\uc640 endPage\ub9cc \uc7ac\uacc4\uc0b0\ub418\uace0 prev\uc640 next\ub294 \uc720\uc9c0\ub41c\ub2e4.", "\ud544\ub4dc\ub9cc \ubcc0\uacbd\ub418\uba70 startPage, endPage, prev, next\ub294 \uc790\ub3d9\uc73c\ub85c \uc7ac\uacc4\uc0b0\ub418\uc9c0 \uc54a\ub294\ub2e4.", "\ud30c\uc0dd \uac12 \ubcc0\uacbd\uc774 \uae08\uc9c0\ub418\uc5b4 \ucef4\ud30c\uc77c \uc624\ub958\uac00 \ubc1c\uc0dd\ud55c\ub2e4."]', 'java', '2026-08-02 11:22:18.079452', '2026-08-02 11:22:18.079459', NULL, NULL, NULL, NULL, NULL, NULL, NULL, false),
	(271, 4, 'CODE', '생성자 실행 후 페이지네이션 값 계산', 'pgvo.getPageNo()가 15, pgvo.getQty()가 10, totalCount가 235일 때 PagingHandler 생성 직후의 startPage, endPage, prev, next 값으로 올바른 것은 무엇입니까?', '0', '초기 endPage는 ceil(15/10.0)×10=20이고, startPage는 20-9=11입니다. 전체 마지막 페이지인 realEndPage는 ceil(235/10.0)=24이므로 endPage는 20으로 유지됩니다. startPage가 1보다 크므로 prev는 true이고, endPage 20이 realEndPage 24보다 작으므로 next도 true입니다.', 'MEDIUM', 'PagingHandler.java', '["startPage=11, endPage=20, prev=true, next=true", "startPage=10, endPage=20, prev=false, next=true", "startPage=11, endPage=24, prev=true, next=false", "startPage=1, endPage=20, prev=false, next=true"]', 'java', '2026-08-02 11:32:12.252531', '2026-08-02 11:32:12.252536', NULL, NULL, NULL, 'package handler;

import domain.PagingVO;

public class PagingHandler {

	private int startPage; //현재 화면에서 보여줄 시작 페이지네이션의 번호
	private int endPage; //현재 화면에서 보여줄 마지막 페이지네이션의 번호
	private boolean prev, next; //이전, 다음 존재 여부
	
	private int totalCount; //총 글수
	private PagingVO pgvo; //pagingVO
	
	public PagingHandler(PagingVO pgvo, int totalCount) {
		this.pgvo = pgvo;
		this.totalCount = totalCount;
		// 페이지번호 / 한 화면의 개시글 수 * 한 화면의 개시글 수
		// 1~10까지는 10, 11~20까지는 20, (5/10)*10 = 10
		// 한 화면에 10개씩 보여짐
		// 한 화면에 보여지는 페이지네이션 마지막 번호 
		this.endPage 
		= (int)Math.ceil(pgvo.getPageNo() / (pgvo.getQty()*1.0))*pgvo.getQty();
		//한 화면에 보여지는 페이지네이션 첫 번호
		this.startPage = this.endPage - 9; 
		int realEndPage = (int)(Math.ceil((totalCount*1.0)/pgvo.getQty())); //페이지네이션의 전체 끝 페이지
		if(realEndPage < this.endPage) {
			this.endPage = realEndPage;
		}
		this.prev = this.startPage > 1; //존재여부
		this.next = this.endPage < realEndPage; 		
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public boolean isPrev() {
		return prev;
	}

	public void setPrev(boolean prev) {
		this.prev = prev;
	}

	public boolean isNext() {
		return next;
	}

	public void setNext(boolean next) {
		this.next = next;
	}

	public int getTotalCount() {
		return totalCount;
	}

	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	public PagingVO getPgvo() {
		return pgvo;
	}

	public void setPgvo(PagingVO pgvo) {
		this.pgvo = pgvo;
	}
	
	
	
}
', NULL, 1, NULL, false),
	(272, 4, 'CODE', '전체 마지막 페이지 계산', 'totalCount가 101이고 pgvo.getQty()가 10일 때 생성자에서 계산되는 realEndPage 값은 무엇입니까?', '1', 'realEndPage는 ceil((totalCount×1.0)/qty)로 계산됩니다. 따라서 ceil(101/10.0)=ceil(10.1)=11입니다. 마지막 한 개의 게시글도 별도의 페이지가 필요하므로 총 11페이지입니다.', 'EASY', 'PagingHandler.java', '["10", "11", "101", "110"]', 'java', '2026-08-02 11:32:12.252538', '2026-08-02 11:32:12.252541', NULL, NULL, NULL, 'package handler;

import domain.PagingVO;

public class PagingHandler {

	private int startPage; //현재 화면에서 보여줄 시작 페이지네이션의 번호
	private int endPage; //현재 화면에서 보여줄 마지막 페이지네이션의 번호
	private boolean prev, next; //이전, 다음 존재 여부
	
	private int totalCount; //총 글수
	private PagingVO pgvo; //pagingVO
	
	public PagingHandler(PagingVO pgvo, int totalCount) {
		this.pgvo = pgvo;
		this.totalCount = totalCount;
		// 페이지번호 / 한 화면의 개시글 수 * 한 화면의 개시글 수
		// 1~10까지는 10, 11~20까지는 20, (5/10)*10 = 10
		// 한 화면에 10개씩 보여짐
		// 한 화면에 보여지는 페이지네이션 마지막 번호 
		this.endPage 
		= (int)Math.ceil(pgvo.getPageNo() / (pgvo.getQty()*1.0))*pgvo.getQty();
		//한 화면에 보여지는 페이지네이션 첫 번호
		this.startPage = this.endPage - 9; 
		int realEndPage = (int)(Math.ceil((totalCount*1.0)/pgvo.getQty())); //페이지네이션의 전체 끝 페이지
		if(realEndPage < this.endPage) {
			this.endPage = realEndPage;
		}
		this.prev = this.startPage > 1; //존재여부
		this.next = this.endPage < realEndPage; 		
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public boolean isPrev() {
		return prev;
	}

	public void setPrev(boolean prev) {
		this.prev = prev;
	}

	public boolean isNext() {
		return next;
	}

	public void setNext(boolean next) {
		this.next = next;
	}

	public int getTotalCount() {
		return totalCount;
	}

	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	public PagingVO getPgvo() {
		return pgvo;
	}

	public void setPgvo(PagingVO pgvo) {
		this.pgvo = pgvo;
	}
	
	
	
}
', NULL, 2, NULL, false),
	(273, 4, 'CODE', '이전 및 다음 페이지네이션 존재 여부', 'pgvo.getPageNo()가 7, pgvo.getQty()가 10, totalCount가 95일 때 prev와 next의 값으로 올바른 것은 무엇입니까?', '2', 'endPage는 ceil(7/10.0)×10=10이고 startPage는 10-9=1입니다. realEndPage도 ceil(95/10.0)=10입니다. startPage가 1보다 크지 않으므로 prev는 false이며, endPage가 realEndPage보다 작지 않으므로 next도 false입니다.', 'MEDIUM', 'PagingHandler.java', '["prev=true, next=true", "prev=true, next=false", "prev=false, next=false", "prev=false, next=true"]', 'java', '2026-08-02 11:32:12.252544', '2026-08-02 11:32:12.252546', NULL, NULL, NULL, 'package handler;

import domain.PagingVO;

public class PagingHandler {

	private int startPage; //현재 화면에서 보여줄 시작 페이지네이션의 번호
	private int endPage; //현재 화면에서 보여줄 마지막 페이지네이션의 번호
	private boolean prev, next; //이전, 다음 존재 여부
	
	private int totalCount; //총 글수
	private PagingVO pgvo; //pagingVO
	
	public PagingHandler(PagingVO pgvo, int totalCount) {
		this.pgvo = pgvo;
		this.totalCount = totalCount;
		// 페이지번호 / 한 화면의 개시글 수 * 한 화면의 개시글 수
		// 1~10까지는 10, 11~20까지는 20, (5/10)*10 = 10
		// 한 화면에 10개씩 보여짐
		// 한 화면에 보여지는 페이지네이션 마지막 번호 
		this.endPage 
		= (int)Math.ceil(pgvo.getPageNo() / (pgvo.getQty()*1.0))*pgvo.getQty();
		//한 화면에 보여지는 페이지네이션 첫 번호
		this.startPage = this.endPage - 9; 
		int realEndPage = (int)(Math.ceil((totalCount*1.0)/pgvo.getQty())); //페이지네이션의 전체 끝 페이지
		if(realEndPage < this.endPage) {
			this.endPage = realEndPage;
		}
		this.prev = this.startPage > 1; //존재여부
		this.next = this.endPage < realEndPage; 		
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public boolean isPrev() {
		return prev;
	}

	public void setPrev(boolean prev) {
		this.prev = prev;
	}

	public boolean isNext() {
		return next;
	}

	public void setNext(boolean next) {
		this.next = next;
	}

	public int getTotalCount() {
		return totalCount;
	}

	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	public PagingVO getPgvo() {
		return pgvo;
	}

	public void setPgvo(PagingVO pgvo) {
		this.pgvo = pgvo;
	}
	
	
	
}
', NULL, 3, NULL, false),
	(274, 4, 'CODE', 'qty가 20일 때의 페이지 범위', 'pgvo.getPageNo()가 21, pgvo.getQty()가 20, totalCount가 1000일 때 생성 직후 startPage와 endPage는 무엇입니까?', '3', 'endPage는 ceil(21/20.0)×20=40입니다. startPage 계산에는 qty가 사용되지 않고 코드에 고정된 9를 빼므로 40-9=31입니다. realEndPage는 ceil(1000/20.0)=50이어서 기존 endPage 40이 변경되지 않습니다.', 'HARD', 'PagingHandler.java', '["startPage=21, endPage=40", "startPage=21, endPage=30", "startPage=20, endPage=40", "startPage=31, endPage=40"]', 'java', '2026-08-02 11:32:12.252548', '2026-08-02 11:32:12.25255', NULL, NULL, NULL, 'package handler;

import domain.PagingVO;

public class PagingHandler {

	private int startPage; //현재 화면에서 보여줄 시작 페이지네이션의 번호
	private int endPage; //현재 화면에서 보여줄 마지막 페이지네이션의 번호
	private boolean prev, next; //이전, 다음 존재 여부
	
	private int totalCount; //총 글수
	private PagingVO pgvo; //pagingVO
	
	public PagingHandler(PagingVO pgvo, int totalCount) {
		this.pgvo = pgvo;
		this.totalCount = totalCount;
		// 페이지번호 / 한 화면의 개시글 수 * 한 화면의 개시글 수
		// 1~10까지는 10, 11~20까지는 20, (5/10)*10 = 10
		// 한 화면에 10개씩 보여짐
		// 한 화면에 보여지는 페이지네이션 마지막 번호 
		this.endPage 
		= (int)Math.ceil(pgvo.getPageNo() / (pgvo.getQty()*1.0))*pgvo.getQty();
		//한 화면에 보여지는 페이지네이션 첫 번호
		this.startPage = this.endPage - 9; 
		int realEndPage = (int)(Math.ceil((totalCount*1.0)/pgvo.getQty())); //페이지네이션의 전체 끝 페이지
		if(realEndPage < this.endPage) {
			this.endPage = realEndPage;
		}
		this.prev = this.startPage > 1; //존재여부
		this.next = this.endPage < realEndPage; 		
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public boolean isPrev() {
		return prev;
	}

	public void setPrev(boolean prev) {
		this.prev = prev;
	}

	public boolean isNext() {
		return next;
	}

	public void setNext(boolean next) {
		this.next = next;
	}

	public int getTotalCount() {
		return totalCount;
	}

	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	public PagingVO getPgvo() {
		return pgvo;
	}

	public void setPgvo(PagingVO pgvo) {
		this.pgvo = pgvo;
	}
	
	
	
}
', NULL, 4, NULL, false),
	(275, 4, 'CODE', 'totalCount 설정자 호출의 영향', 'pgvo.getPageNo()가 15, pgvo.getQty()가 10인 객체를 totalCount=235로 생성한 직후 setTotalCount(95)를 호출했습니다. 이후 상태에 대한 설명으로 올바른 것은 무엇입니까?', '1', 'setTotalCount 메서드는 this.totalCount = totalCount만 실행합니다. 페이지 범위와 prev, next를 다시 계산하는 코드는 생성자에만 있으므로, setTotalCount(95)를 호출해도 기존 startPage=11, endPage=20, prev=true, next=true는 그대로 유지되고 totalCount만 95로 변경됩니다.', 'HARD', 'PagingHandler.java', '["endPage가 10으로 다시 계산되고 next가 false가 된다.", "totalCount만 95로 바뀌고 startPage, endPage, prev, next는 자동으로 다시 계산되지 않는다.", "pgvo의 qty도 95로 변경된다.", "startPage와 endPage가 모두 95로 변경된다."]', 'java', '2026-08-02 11:32:12.252552', '2026-08-02 11:32:12.252554', NULL, NULL, NULL, 'package handler;

import domain.PagingVO;

public class PagingHandler {

	private int startPage; //현재 화면에서 보여줄 시작 페이지네이션의 번호
	private int endPage; //현재 화면에서 보여줄 마지막 페이지네이션의 번호
	private boolean prev, next; //이전, 다음 존재 여부
	
	private int totalCount; //총 글수
	private PagingVO pgvo; //pagingVO
	
	public PagingHandler(PagingVO pgvo, int totalCount) {
		this.pgvo = pgvo;
		this.totalCount = totalCount;
		// 페이지번호 / 한 화면의 개시글 수 * 한 화면의 개시글 수
		// 1~10까지는 10, 11~20까지는 20, (5/10)*10 = 10
		// 한 화면에 10개씩 보여짐
		// 한 화면에 보여지는 페이지네이션 마지막 번호 
		this.endPage 
		= (int)Math.ceil(pgvo.getPageNo() / (pgvo.getQty()*1.0))*pgvo.getQty();
		//한 화면에 보여지는 페이지네이션 첫 번호
		this.startPage = this.endPage - 9; 
		int realEndPage = (int)(Math.ceil((totalCount*1.0)/pgvo.getQty())); //페이지네이션의 전체 끝 페이지
		if(realEndPage < this.endPage) {
			this.endPage = realEndPage;
		}
		this.prev = this.startPage > 1; //존재여부
		this.next = this.endPage < realEndPage; 		
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public boolean isPrev() {
		return prev;
	}

	public void setPrev(boolean prev) {
		this.prev = prev;
	}

	public boolean isNext() {
		return next;
	}

	public void setNext(boolean next) {
		this.next = next;
	}

	public int getTotalCount() {
		return totalCount;
	}

	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	public PagingVO getPgvo() {
		return pgvo;
	}

	public void setPgvo(PagingVO pgvo) {
		this.pgvo = pgvo;
	}
	
	
	
}
', NULL, 2, NULL, false),
	(276, 4, 'EXCEL', '기본구문(조건문, 반복문)', '다음 자바 코드의 실행 결과로 올바른 것은?', '1', '5 % 2는 1이므로 else 문이 실행되어 Odd가 출력됩니다.', 'EASY', 'sample (1).xlsx', '["Even", "Odd", "null", "컴파일 에러"]', 'Java,If-Else', '2026-08-03 15:43:11.615801', '2026-08-03 15:43:11.615811', 1, 'JAVA', '기본구문(조건문, 반복문)', 'int a = 5;
if (a % 2 == 0) {
    System.out.println("Even");
} else {
    System.out.println("Odd");
}', 45, 2, NULL, true),
	(277, 4, 'EXCEL', '컬렉션(List)', '다음 중 Java에서 ArrayList를 생성하는 올바른 코드는?', '1', 'List는 인터페이스이므로 ArrayList 구현체를 생성하여 대입할 수 있습니다.', 'MEDIUM', 'sample (1).xlsx', '["List<String> names = new List<>();", "List<String> names = new ArrayList<>();", "ArrayList names = ArrayList();", "List names = new String[];"]', 'Java,List,ArrayList', '2026-08-03 15:43:11.625141', '2026-08-03 15:43:11.625144', 2, 'JAVA', '컬렉션(List)', 'List<String> names = new ArrayList<>();', 30, 2, NULL, false);


--
-- Data for Name: excel_questions; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.excel_questions (id, question_id, excel_row_number, file_name, created_at) VALUES
	(1, 276, 2, 'sample (1).xlsx', '2026-08-03 15:43:11.621961'),
	(2, 277, 3, 'sample (1).xlsx', '2026-08-03 15:43:11.666551');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users (id, name, phone, email, password_hash, role, created_at) VALUES
	(1, 'admin', '000-0000-0000', 'admin@example.com', 'pbkdf2_sha256$600000$f11b47fa516e742d61aefa9e6733839f$050752dd53c715bdb9bdc9cec455abb87bf320459b408db2c7a7a7f90411fd35', 'ADMIN', '2026-07-30 12:14:48.258886'),
	(2, '오미란', '010-3512-5093', 'test@never.com', 'pbkdf2_sha256$600000$57c102f89c16c2c15363363c29e52e85$2e197b0db5236125c39ea9749722ce61f7d170f3e0bbb4136afa22c8cff7beac', 'STUDENT', '2026-07-30 12:21:12.178102'),
	(3, '오미란', '010-1111-1111', 'pro@gmail.com', 'pbkdf2_sha256$600000$42bd09a02b65d26134598f25701fed20$d6c4a9cef9c66c63ea1d554d3075e154734651abf1b85f176ece10fe2621c4d9', 'PROFESSOR', '2026-07-30 13:12:01.238895'),
	(4, '김민준', '010-8000-0001', 'adaptive.student01@example.com', 'pbkdf2_sha256$600000$67edd80caa3fdeab9da94addf2697bcf$d7f941d673d905492ab505e5750cb3b8183a67c0e57e0ff00e2eaef92fe3ab7a', 'STUDENT', '2026-08-03 04:21:48.85675'),
	(5, '이서연', '010-8000-0002', 'adaptive.student02@example.com', 'pbkdf2_sha256$600000$d647d032988b6587fbcc2528d4ff630c$2e5f30c97f78a20f352b37688ea7526f77e38af63e3f0dc0d96a92d2b4df829d', 'STUDENT', '2026-08-03 04:21:49.167905'),
	(6, '박지후', '010-8000-0003', 'adaptive.student03@example.com', 'pbkdf2_sha256$600000$4e4400d79c28498584c79b903c09ff0d$056aa7410a905292331963935c7747392c8fc8b5660faf9c32bedd2f5eeac327', 'STUDENT', '2026-08-03 04:21:49.447699'),
	(7, '최하윤', '010-8000-0004', 'adaptive.student04@example.com', 'pbkdf2_sha256$600000$400368ec7839058067276175cdcbdd8e$8842579442968b86016599462a9b54cff5aba76b7cf612f333f6f00911b29df9', 'STUDENT', '2026-08-03 04:21:49.71978'),
	(8, '정도윤', '010-8000-0005', 'adaptive.student05@example.com', 'pbkdf2_sha256$600000$dc926489c12773c35f493be65ebbcaf8$b5f39526706b8734048ff5cd4ec4c5dacfd7db482f53cd0402e0e56d777db75d', 'STUDENT', '2026-08-03 04:21:49.996649'),
	(9, '강지아', '010-8000-0006', 'adaptive.student06@example.com', 'pbkdf2_sha256$600000$24e6854dcb07ec17ee191dbd61f47d7e$35656a63043b9419085e6f5d6bdb7fcbb506a57469a56ba70b48afbf24ed47f9', 'STUDENT', '2026-08-03 04:21:50.27094'),
	(10, '조현우', '010-8000-0007', 'adaptive.student07@example.com', 'pbkdf2_sha256$600000$dcc0425c9aff0f517939203d5be9c415$e65c05b1fc8efffe3aaa6366f40812e5f2664a587ee1bc9946407a3b00dba5e4', 'STUDENT', '2026-08-03 04:21:50.557534'),
	(11, '윤서아', '010-8000-0008', 'adaptive.student08@example.com', 'pbkdf2_sha256$600000$6e9b4aa8a8c81438e5d16530d9a5104e$3c466da8df0952f9ae9069575acfa489ff6fcc238b1ddc2780159bc444caddbe', 'STUDENT', '2026-08-03 04:21:50.849018'),
	(12, '장시우', '010-8000-0009', 'adaptive.student09@example.com', 'pbkdf2_sha256$600000$825d69028db3ee8ccf318f69cd6ec1c0$33d404207b9d26e161bc0a7a4dd9c275d4736345a29a875a1f552a1a1aef7ad2', 'STUDENT', '2026-08-03 04:21:51.121647'),
	(13, '임채원', '010-8000-0010', 'adaptive.student10@example.com', 'pbkdf2_sha256$600000$ed28b3d7bed2e9b057c0999680b9e7d2$46d34c8bb2feda22fbe2f8e8a88ddfe78ddff5481cbbd2dbeba36a0e64fb51ee', 'STUDENT', '2026-08-03 04:21:51.409134');


--
-- Data for Name: quiz_sessions; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.quiz_sessions (id, user_id, total_seconds, total_questions, correct_answers, score_percent, achievement_score, completed_at) VALUES
	('2c978c91-f1f9-4c00-96aa-70665373c204', 2, 34.763, 5, 4, 80, 100, '2026-07-30 12:51:00.769723'),
	('bb705fb9-6802-422e-849c-80634ee3f909', 2, 50.954, 5, 4, 80, 112.5, '2026-07-30 13:02:10.253569'),
	('a59df9e6-c71a-4c56-8040-06c4eb5b0e09', 2, 39.312, 5, 4, 80, 100, '2026-07-31 04:51:23.189374'),
	('c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 4, 601.6, 10, 6, 60, 60, '2026-06-23 05:21:48.864082'),
	('9a42448a-18c0-4ada-bb9c-8818da280a6f', 4, 628.7, 10, 8, 80, 80, '2026-06-24 05:21:48.864082'),
	('3e4006ed-a751-4514-b589-02b3ed75cc13', 4, 631.9, 10, 6, 60, 60, '2026-06-25 05:21:48.864082'),
	('fbaff450-febb-4d8f-8f70-21cdecb08637', 4, 582.9, 10, 8, 80, 80, '2026-06-26 05:21:48.864082'),
	('792087a0-1cae-406c-81e2-bbe24efb102a', 4, 547.9, 10, 7, 70, 70, '2026-06-27 05:21:48.864082'),
	('5ac63d5d-0336-42bc-8dd9-451e836c22d1', 4, 563.8, 10, 8, 80, 80, '2026-06-28 05:21:48.864082'),
	('7a67767a-3d2f-492e-8458-d7e8763b3941', 4, 274.1, 4, 1, 25, 25, '2026-06-29 05:21:48.864082'),
	('7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 5, 705.3, 10, 6, 60, 60, '2026-06-22 05:21:49.178083'),
	('f7b458ae-3865-4038-84c3-9d52b94847f6', 5, 527.8, 10, 10, 100, 100, '2026-06-23 05:21:49.178083'),
	('73126b44-729b-495b-a196-d375a3bf9824', 5, 636.4, 10, 5, 50, 50, '2026-06-24 05:21:49.178083'),
	('b4075750-10d6-4d23-bb8e-d10519829d6e', 5, 607.5, 10, 3, 30, 30, '2026-06-25 05:21:49.178083'),
	('abf1c635-119c-4b53-b25c-e11cabbe999a', 5, 591.1, 10, 7, 70, 70, '2026-06-26 05:21:49.178083'),
	('142772bf-90b3-41d5-b1b5-3fb73be452b0', 5, 708.6, 10, 5, 50, 50, '2026-06-27 05:21:49.178083'),
	('51d5976b-c979-4288-8bd7-96daa2aa4836', 5, 608.9, 10, 8, 80, 80, '2026-06-28 05:21:49.178083'),
	('971ac233-89fb-4358-85e3-76e8f1013374', 6, 528.2, 10, 7, 70, 70, '2026-07-11 05:21:49.455531'),
	('7fa40372-7716-4e3e-b884-699ef3004763', 6, 619, 10, 5, 50, 50, '2026-07-12 05:21:49.455531'),
	('5b5904a2-0152-42b1-97ed-36554b8a16b0', 6, 553.2, 10, 6, 60, 60, '2026-07-13 05:21:49.455531'),
	('25887c15-636b-48df-bfad-631087f9bdea', 6, 739.2, 10, 6, 60, 60, '2026-07-14 05:21:49.455531'),
	('35774bf9-987c-41eb-af77-0059b37acfb4', 6, 600.7, 10, 7, 70, 70, '2026-07-15 05:21:49.455531'),
	('40a75e2d-8068-4792-a183-df895c954cef', 6, 564.5, 8, 7, 88, 88, '2026-07-16 05:21:49.455531'),
	('6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 7, 609.9, 10, 7, 70, 70, '2026-06-21 05:21:49.725771'),
	('595b812a-d520-43e9-bed4-0e4b5625c3a4', 7, 624.4, 10, 7, 70, 70, '2026-06-22 05:21:49.725771'),
	('d6bb7213-8e5f-4732-a149-e361b15e2c79', 7, 622.9, 10, 7, 70, 70, '2026-06-23 05:21:49.725771'),
	('39396972-498d-47c0-8ac6-207077a6027a', 7, 659.6, 10, 7, 70, 70, '2026-06-24 05:21:49.725771'),
	('ac33459f-3307-4008-9ac4-8d130686564f', 7, 566.6, 10, 4, 40, 40, '2026-06-25 05:21:49.725771'),
	('7d215071-2247-4c4d-b4be-d034b28975dc', 7, 588, 10, 7, 70, 70, '2026-06-26 05:21:49.725771'),
	('48170fe0-4c6b-4a87-9558-b0d9cdadb667', 7, 517, 10, 7, 70, 70, '2026-06-27 05:21:49.725771'),
	('1b41f244-e506-4278-a50f-940ac8c3e1b9', 7, 751.7, 10, 6, 60, 60, '2026-06-28 05:21:49.725771'),
	('0b624a7f-5031-425d-a800-e599fa0b6af0', 7, 83.4, 1, 0, 0, 0, '2026-06-29 05:21:49.725771'),
	('5bb3bee5-c69a-408d-a449-e83d3962d527', 8, 545.6, 10, 6, 60, 60, '2026-06-25 05:21:50.004229'),
	('c708259d-30ed-4cbb-bfee-4c7469d8c95b', 8, 588.1, 10, 5, 50, 50, '2026-06-26 05:21:50.004229'),
	('838ea203-5965-4503-8b7c-3a1526aff1cc', 8, 621.7, 10, 7, 70, 70, '2026-06-27 05:21:50.004229'),
	('c19c9f92-1f07-4602-9a81-8cb701bd47ba', 8, 589.5, 10, 7, 70, 70, '2026-06-28 05:21:50.004229'),
	('232b2f64-7d3b-4e73-8d13-a0c9655587b4', 8, 562, 10, 8, 80, 80, '2026-06-29 05:21:50.004229'),
	('5728978a-3d63-41b8-b974-14cc01d7d27a', 8, 614.5, 10, 6, 60, 60, '2026-06-30 05:21:50.004229'),
	('ae83a0ed-e76f-407d-aeac-628cb097cb71', 8, 553.4, 8, 4, 50, 50, '2026-07-01 05:21:50.004229'),
	('c3e483ff-feae-4181-ac67-4b4eb6f37818', 9, 538.9, 10, 7, 70, 70, '2026-07-01 05:21:50.277866'),
	('6687b44b-6cd2-456e-84b9-24fe4fedc423', 9, 621.4, 10, 6, 60, 60, '2026-07-02 05:21:50.277866'),
	('86c4e780-4a1a-4041-8ab5-18c499d39eb8', 9, 564.9, 10, 7, 70, 70, '2026-07-03 05:21:50.277866'),
	('044c19a4-44f5-4af2-8d17-3c573e928a84', 9, 517.2, 10, 3, 30, 30, '2026-07-04 05:21:50.277866'),
	('eae3b4a5-5f3b-4a03-bb73-c602e792da96', 9, 748.4, 10, 3, 30, 30, '2026-07-05 05:21:50.277866'),
	('1c0ca879-edd4-4e89-9621-478a2bdeeb95', 9, 579.8, 10, 6, 60, 60, '2026-07-06 05:21:50.277866'),
	('17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 10, 494.8, 10, 5, 50, 50, '2026-06-22 05:21:50.566609'),
	('67c6db24-b249-469e-82ec-b8cdaa009c68', 10, 616.9, 10, 7, 70, 70, '2026-06-23 05:21:50.566609'),
	('e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 10, 582.5, 10, 4, 40, 40, '2026-06-24 05:21:50.566609'),
	('2965e48a-d30b-45c5-b440-5df6377439df', 10, 662.5, 10, 5, 50, 50, '2026-06-25 05:21:50.566609'),
	('4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 10, 583.9, 10, 4, 40, 40, '2026-06-26 05:21:50.566609'),
	('2149eb46-fa12-48d1-a071-24acfe8d6bc6', 10, 566.8, 10, 4, 40, 40, '2026-06-27 05:21:50.566609'),
	('0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 10, 673, 10, 1, 10, 10, '2026-06-28 05:21:50.566609'),
	('ec6b9009-b8dd-4233-bbc0-2374bc7b93ee', 10, 137.3, 3, 2, 67, 67, '2026-06-29 05:21:50.566609'),
	('c646131e-c6ed-408b-ada0-97fb1a6f40f2', 11, 511.8, 10, 2, 20, 20, '2026-07-13 05:21:50.856868'),
	('0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 11, 598.1, 10, 4, 40, 40, '2026-07-14 05:21:50.856868'),
	('65585ff9-e02e-4f55-8fae-125a33375e3a', 11, 631.6, 10, 3, 30, 30, '2026-07-15 05:21:50.856868'),
	('b964139b-48f3-4612-b27e-ee5c55777e54', 11, 527.6, 10, 2, 20, 20, '2026-07-16 05:21:50.856868'),
	('1f21af38-376a-438d-badf-12e6cb078de1', 11, 599.2, 10, 5, 50, 50, '2026-07-17 05:21:50.856868'),
	('8db28499-6ff4-4709-adb1-269a14e476ae', 11, 577.4, 10, 2, 20, 20, '2026-07-18 05:21:50.856868'),
	('c64b1a92-5590-43b6-a527-a9071cc55914', 11, 673.7, 10, 6, 60, 60, '2026-07-19 05:21:50.856868'),
	('a32892a1-5ecf-4747-b24f-2dace7d8f1c3', 11, 355.8, 7, 3, 43, 43, '2026-07-20 05:21:50.856868'),
	('8e0701e5-6483-45d2-9b99-046394e8094d', 12, 677.4, 10, 4, 40, 40, '2026-06-23 05:21:51.128294'),
	('774c5a54-078e-440e-907f-487efee6e16a', 12, 589.1, 10, 1, 10, 10, '2026-06-24 05:21:51.128294'),
	('a36c6bad-4bde-4251-a47a-0ea8c1474053', 12, 651.4, 10, 3, 30, 30, '2026-06-25 05:21:51.128294'),
	('3f9cf661-4e99-4675-97b1-b61da4a84b1c', 12, 634.4, 10, 3, 30, 30, '2026-06-26 05:21:51.128294'),
	('c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 12, 563.5, 10, 3, 30, 30, '2026-06-27 05:21:51.128294'),
	('9cddb0ce-79e0-4694-a929-e10aee88e063', 12, 576, 10, 7, 70, 70, '2026-06-28 05:21:51.128294'),
	('d82bc375-fd2d-41f6-969d-61e49aadd51b', 12, 629.5, 10, 4, 40, 40, '2026-06-29 05:21:51.128294'),
	('b609f374-9f99-4e99-bcdd-eb17c3be8c77', 12, 344.1, 5, 3, 60, 60, '2026-06-30 05:21:51.128294'),
	('d7002106-4e6e-4552-a283-443bbd3bbb8f', 13, 639.9, 10, 2, 20, 20, '2026-07-21 05:21:51.41577'),
	('9320011d-7013-43cf-bc20-78066b012a14', 13, 709.6, 10, 2, 20, 20, '2026-07-22 05:21:51.41577'),
	('26f55756-b0fd-4cf1-8572-9f5a3d645430', 13, 474.6, 10, 4, 40, 40, '2026-07-23 05:21:51.41577'),
	('44d2f217-0fed-4ba1-810c-967f65696644', 13, 608.4, 10, 3, 30, 30, '2026-07-24 05:21:51.41577'),
	('c6f27d02-fb39-465a-8103-99ee1a84bd67', 13, 590.7, 10, 2, 20, 20, '2026-07-25 05:21:51.41577'),
	('5e929969-d24e-4633-b7ee-f034b08a0437', 13, 589.5, 10, 4, 40, 40, '2026-07-26 05:21:51.41577'),
	('429310fc-1167-4831-89b4-c63829f06fc4', 13, 583.3, 10, 0, 0, 0, '2026-07-27 05:21:51.41577'),
	('facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 13, 577.5, 10, 2, 20, 20, '2026-07-28 05:21:51.41577'),
	('2bf2cbf8-3b1d-4d5f-aaff-183f19784498', 2, 67.093, 5, 2, 40, 67.5, '2026-08-03 07:04:46.017086'),
	('6e00f5b9-97a0-492f-b437-bce67a0ace66', 2, 71.619, 5, 4, 80, 100, '2026-08-03 07:50:50.985695'),
	('342ea4b9-9dad-4b3c-ae3b-17e299399f70', 2, 139.593, 10, 7, 70, 115.05, '2026-08-03 12:07:35.584601'),
	('7377fc66-0bdf-4c29-a573-872f1bf67cec', 2, 35.268, 5, 4, 80, 100, '2026-08-03 12:11:51.757622'),
	('2d9520e6-912e-4b29-9ab3-8ab1919b7559', 2, 3.08, 1, 1, 100, 125, '2026-08-03 12:12:32.528297'),
	('e5eb6f34-f312-407f-8d55-064d2d306855', 2, 7.693, 1, 1, 100, 150, '2026-08-04 07:36:37.423852'),
	('6049b21d-464d-41f6-a29f-1eb23d0d5c34', 2, 2.79, 1, 1, 100, 150, '2026-08-04 07:42:18.697459'),
	('3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 2, 60.508, 10, 5, 50, 72.5, '2026-08-04 10:19:39.32844');


--
-- Data for Name: user_progress; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(4, '2', 31, 'INCORRECT', '0', '2026-07-30 12:51:00.77431', '2c978c91-f1f9-4c00-96aa-70665373c204', 1, 6.13, 0),
	(5, '2', 61, 'CORRECT', '1', '2026-07-30 12:51:00.774315', '2c978c91-f1f9-4c00-96aa-70665373c204', 2, 11.84, 125),
	(6, '2', 62, 'CORRECT', '0', '2026-07-30 12:51:00.774318', '2c978c91-f1f9-4c00-96aa-70665373c204', 3, 4.98, 125),
	(7, '2', 51, 'CORRECT', '2', '2026-07-30 12:51:00.774321', '2c978c91-f1f9-4c00-96aa-70665373c204', 4, 7.99, 125),
	(8, '2', 20, 'CORRECT', '3', '2026-07-30 12:51:00.774323', '2c978c91-f1f9-4c00-96aa-70665373c204', 5, 3.82, 125),
	(9, '2', 72, 'CORRECT', '1', '2026-07-30 13:02:10.254344', 'bb705fb9-6802-422e-849c-80634ee3f909', 1, 10.7, 125),
	(10, '2', 203, 'INCORRECT', '1', '2026-07-30 13:02:10.254348', 'bb705fb9-6802-422e-849c-80634ee3f909', 2, 7.52, 0),
	(11, '2', 41, 'CORRECT', '1', '2026-07-30 13:02:10.254349', 'bb705fb9-6802-422e-849c-80634ee3f909', 3, 5.61, 125),
	(12, '2', 23, 'CORRECT', '2', '2026-07-30 13:02:10.254351', 'bb705fb9-6802-422e-849c-80634ee3f909', 4, 19.81, 187.5),
	(13, '2', 169, 'CORRECT', '0', '2026-07-30 13:02:10.254353', 'bb705fb9-6802-422e-849c-80634ee3f909', 5, 7.32, 125),
	(14, '2', 226, 'CORRECT', '0', '2026-07-31 04:51:23.200477', 'a59df9e6-c71a-4c56-8040-06c4eb5b0e09', 1, 6.56, 125),
	(15, '2', 231, 'CORRECT', '0', '2026-07-31 04:51:23.200481', 'a59df9e6-c71a-4c56-8040-06c4eb5b0e09', 2, 6.09, 125),
	(16, '2', 255, 'CORRECT', '0', '2026-07-31 04:51:23.200483', 'a59df9e6-c71a-4c56-8040-06c4eb5b0e09', 3, 6.18, 125),
	(17, '2', 184, 'CORRECT', '0', '2026-07-31 04:51:23.200485', 'a59df9e6-c71a-4c56-8040-06c4eb5b0e09', 4, 6.67, 125),
	(18, '2', 195, 'INCORRECT', '1', '2026-07-31 04:51:23.200487', 'a59df9e6-c71a-4c56-8040-06c4eb5b0e09', 5, 13.82, 0),
	(19, '4', 11, 'INCORRECT', '3', '2026-06-23 04:23:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 1, 76.3, 0),
	(20, '4', 68, 'CORRECT', '2', '2026-06-23 04:25:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 2, 80, 100),
	(21, '4', 56, 'CORRECT', '1', '2026-06-23 04:27:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 3, 103, 100),
	(22, '4', 46, 'INCORRECT', '3', '2026-06-23 04:29:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 4, 40.8, 0),
	(23, '4', 216, 'CORRECT', '0', '2026-06-23 04:31:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 5, 67.3, 100),
	(25, '4', 13, 'INCORRECT', '3', '2026-06-23 04:35:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 7, 65.4, 0),
	(26, '4', 192, 'CORRECT', '0', '2026-06-23 04:37:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 8, 58.4, 100),
	(27, '4', 233, 'CORRECT', '0', '2026-06-23 04:39:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 9, 36.2, 100),
	(28, '4', 181, 'INCORRECT', '0', '2026-06-23 04:41:48.864082', 'c2dfe8d7-8cbe-4d86-a412-8a2610b5007b', 10, 23.2, 0),
	(29, '4', 144, 'CORRECT', '0', '2026-06-24 04:23:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 1, 44.6, 100),
	(30, '4', 173, 'CORRECT', '0', '2026-06-24 04:25:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 2, 74.6, 100),
	(31, '4', 49, 'CORRECT', '1', '2026-06-24 04:27:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 3, 76.4, 100),
	(32, '4', 28, 'CORRECT', '0', '2026-06-24 04:29:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 4, 56.7, 100),
	(34, '4', 76, 'SKIP', NULL, '2026-06-24 04:33:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 6, 60.5, 0),
	(35, '4', 50, 'SKIP', NULL, '2026-06-24 04:35:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 7, 36.6, 0),
	(36, '4', 42, 'CORRECT', '1', '2026-06-24 04:37:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 8, 41.5, 100),
	(37, '4', 105, 'CORRECT', '0', '2026-06-24 04:39:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 9, 45, 100),
	(38, '4', 64, 'CORRECT', '2', '2026-06-24 04:41:48.864082', '9a42448a-18c0-4ada-bb9c-8818da280a6f', 10, 78.2, 100),
	(39, '4', 32, 'INCORRECT', '2', '2026-06-25 04:23:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 1, 66.8, 0),
	(40, '4', 38, 'CORRECT', '1', '2026-06-25 04:25:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 2, 95.7, 100),
	(41, '4', 15, 'CORRECT', '3', '2026-06-25 04:27:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 3, 75.3, 100),
	(42, '4', 167, 'CORRECT', '0', '2026-06-25 04:29:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 4, 67.7, 100),
	(43, '4', 273, 'INCORRECT', '3', '2026-06-25 04:31:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 5, 64.6, 0),
	(44, '4', 232, 'CORRECT', '0', '2026-06-25 04:33:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 6, 21.3, 100),
	(45, '4', 59, 'CORRECT', '1', '2026-06-25 04:35:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 7, 72.2, 100),
	(46, '4', 35, 'CORRECT', '2', '2026-06-25 04:37:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 8, 56, 100),
	(47, '4', 19, 'SKIP', NULL, '2026-06-25 04:39:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 9, 53.9, 0),
	(48, '4', 150, 'INCORRECT', '3', '2026-06-25 04:41:48.864082', '3e4006ed-a751-4514-b589-02b3ed75cc13', 10, 58.4, 0),
	(49, '4', 171, 'CORRECT', '0', '2026-06-26 04:23:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 1, 48.2, 100),
	(50, '4', 63, 'CORRECT', '2', '2026-06-26 04:25:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 2, 51.1, 100),
	(51, '4', 48, 'CORRECT', '1', '2026-06-26 04:27:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 3, 73.1, 100),
	(52, '4', 75, 'CORRECT', '0', '2026-06-26 04:29:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 4, 62, 100),
	(53, '4', 26, 'INCORRECT', '2', '2026-06-26 04:31:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 5, 52.8, 0),
	(54, '4', 14, 'SKIP', NULL, '2026-06-26 04:33:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 6, 52.4, 0),
	(55, '4', 43, 'CORRECT', '2', '2026-06-26 04:35:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 7, 92.3, 100),
	(56, '4', 139, 'CORRECT', '0', '2026-06-26 04:37:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 8, 53.6, 100),
	(57, '4', 266, 'CORRECT', '0', '2026-06-26 04:39:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 9, 54, 100),
	(58, '4', 239, 'CORRECT', '0', '2026-06-26 04:41:48.864082', 'fbaff450-febb-4d8f-8f70-21cdecb08637', 10, 43.4, 100),
	(59, '4', 36, 'CORRECT', '2', '2026-06-27 04:23:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 1, 84.5, 100),
	(60, '4', 10, 'CORRECT', '1', '2026-06-27 04:25:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 2, 20.4, 100),
	(61, '4', 45, 'CORRECT', '0', '2026-06-27 04:27:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 3, 40.5, 100),
	(62, '4', 74, 'INCORRECT', '0', '2026-06-27 04:29:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 4, 28.9, 0),
	(63, '4', 69, 'INCORRECT', '2', '2026-06-27 04:31:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 5, 83.4, 0),
	(64, '4', 41, 'CORRECT', '1', '2026-06-27 04:33:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 6, 48.6, 100),
	(65, '4', 256, 'CORRECT', '0', '2026-06-27 04:35:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 7, 50.6, 100),
	(67, '4', 262, 'INCORRECT', '잘못된 답변', '2026-06-27 04:39:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 9, 60.7, 0),
	(68, '4', 174, 'CORRECT', '0', '2026-06-27 04:41:48.864082', '792087a0-1cae-406c-81e2-bbe24efb102a', 10, 69.4, 100),
	(69, '4', 60, 'CORRECT', '0', '2026-06-28 04:23:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 1, 53.7, 100),
	(71, '4', 34, 'INCORRECT', '1', '2026-06-28 04:27:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 3, 51.4, 0),
	(72, '4', 24, 'CORRECT', '0', '2026-06-28 04:29:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 4, 12.9, 100),
	(73, '4', 225, 'CORRECT', '0', '2026-06-28 04:31:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 5, 52.5, 100),
	(75, '4', 47, 'CORRECT', '3', '2026-06-28 04:35:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 7, 37.5, 100),
	(76, '4', 39, 'CORRECT', '1', '2026-06-28 04:37:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 8, 67.3, 100),
	(77, '4', 55, 'CORRECT', '1', '2026-06-28 04:39:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 9, 67.1, 100),
	(78, '4', 31, 'CORRECT', '1', '2026-06-28 04:41:48.864082', '5ac63d5d-0336-42bc-8dd9-451e836c22d1', 10, 84, 100),
	(79, '4', 240, 'SKIP', NULL, '2026-06-29 04:23:48.864082', '7a67767a-3d2f-492e-8458-d7e8763b3941', 1, 83.6, 0),
	(80, '4', 67, 'CORRECT', '0', '2026-06-29 04:25:48.864082', '7a67767a-3d2f-492e-8458-d7e8763b3941', 2, 35.8, 100),
	(81, '4', 44, 'INCORRECT', '2', '2026-06-29 04:27:48.864082', '7a67767a-3d2f-492e-8458-d7e8763b3941', 3, 46.2, 0),
	(82, '4', 37, 'INCORRECT', '0', '2026-06-29 04:29:48.864082', '7a67767a-3d2f-492e-8458-d7e8763b3941', 4, 108.5, 0),
	(83, '5', 139, 'CORRECT', '0', '2026-06-22 04:23:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 1, 81.3, 100),
	(84, '5', 23, 'INCORRECT', '1', '2026-06-22 04:25:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 2, 100.9, 0),
	(85, '5', 132, 'INCORRECT', '1', '2026-06-22 04:27:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 3, 59.5, 0),
	(86, '5', 96, 'CORRECT', '3', '2026-06-22 04:29:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 4, 103.7, 100),
	(87, '5', 101, 'CORRECT', '1', '2026-06-22 04:31:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 5, 53.1, 100),
	(88, '5', 206, 'INCORRECT', '1', '2026-06-22 04:33:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 6, 31.3, 0),
	(89, '5', 64, 'CORRECT', '2', '2026-06-22 04:35:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 7, 73.5, 100),
	(90, '5', 197, 'CORRECT', '0', '2026-06-22 04:37:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 8, 60.2, 100),
	(91, '5', 232, 'INCORRECT', '1', '2026-06-22 04:39:49.178083', '7a10cd34-b629-4d2f-8bfa-7d818eba61f7', 9, 84.2, 0),
	(93, '5', 226, 'CORRECT', '0', '2026-06-23 04:23:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 1, 39.2, 100),
	(94, '5', 91, 'CORRECT', '1', '2026-06-23 04:25:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 2, 59.7, 100),
	(95, '5', 19, 'CORRECT', '2', '2026-06-23 04:27:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 3, 55.9, 100),
	(96, '5', 51, 'CORRECT', '2', '2026-06-23 04:29:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 4, 33.8, 100),
	(97, '5', 46, 'CORRECT', '1', '2026-06-23 04:31:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 5, 82.1, 100),
	(98, '5', 69, 'CORRECT', '0', '2026-06-23 04:33:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 6, 79.2, 100),
	(99, '5', 200, 'CORRECT', '0', '2026-06-23 04:35:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 7, 45.7, 100),
	(100, '5', 138, 'CORRECT', '0', '2026-06-23 04:37:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 8, 33.9, 100),
	(101, '5', 12, 'CORRECT', '0', '2026-06-23 04:39:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 9, 23.7, 100),
	(102, '5', 130, 'CORRECT', '0', '2026-06-23 04:41:49.178083', 'f7b458ae-3865-4038-84c3-9d52b94847f6', 10, 74.6, 100),
	(103, '5', 59, 'CORRECT', '1', '2026-06-24 04:23:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 1, 99.3, 100),
	(104, '5', 176, 'INCORRECT', '2', '2026-06-24 04:25:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 2, 40.9, 0),
	(105, '5', 146, 'INCORRECT', '2', '2026-06-24 04:27:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 3, 64.5, 0),
	(106, '5', 34, 'CORRECT', '0', '2026-06-24 04:29:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 4, 53.2, 100),
	(107, '5', 20, 'CORRECT', '3', '2026-06-24 04:31:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 5, 52.2, 100),
	(108, '5', 40, 'INCORRECT', '0', '2026-06-24 04:33:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 6, 57, 0),
	(109, '5', 25, 'INCORRECT', '2', '2026-06-24 04:35:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 7, 25.6, 0);
INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(110, '5', 30, 'INCORRECT', '3', '2026-06-24 04:37:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 8, 101, 0),
	(111, '5', 269, 'CORRECT', '1', '2026-06-24 04:39:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 9, 90.2, 100),
	(112, '5', 28, 'CORRECT', '0', '2026-06-24 04:41:49.178083', '73126b44-729b-495b-a196-d375a3bf9824', 10, 52.5, 100),
	(113, '5', 15, 'INCORRECT', '2', '2026-06-25 04:23:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 1, 38.3, 0),
	(114, '5', 56, 'INCORRECT', '3', '2026-06-25 04:25:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 2, 42, 0),
	(115, '5', 218, 'INCORRECT', '2', '2026-06-25 04:27:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 3, 61.9, 0),
	(116, '5', 32, 'INCORRECT', '3', '2026-06-25 04:29:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 4, 55, 0),
	(117, '5', 48, 'INCORRECT', '3', '2026-06-25 04:31:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 5, 57.5, 0),
	(118, '5', 191, 'INCORRECT', '3', '2026-06-25 04:33:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 6, 80.5, 0),
	(119, '5', 57, 'CORRECT', '1', '2026-06-25 04:35:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 7, 84.8, 100),
	(120, '5', 227, 'CORRECT', '0', '2026-06-25 04:37:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 8, 82.1, 100),
	(121, '5', 183, 'CORRECT', '0', '2026-06-25 04:39:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 9, 52.2, 100),
	(122, '5', 111, 'INCORRECT', '3', '2026-06-25 04:41:49.178083', 'b4075750-10d6-4d23-bb8e-d10519829d6e', 10, 53.2, 0),
	(123, '5', 70, 'CORRECT', '3', '2026-06-26 04:23:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 1, 48.2, 100),
	(124, '5', 85, 'INCORRECT', '3', '2026-06-26 04:25:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 2, 65.8, 0),
	(125, '5', 41, 'CORRECT', '1', '2026-06-26 04:27:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 3, 50.8, 100),
	(126, '5', 49, 'SKIP', NULL, '2026-06-26 04:29:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 4, 71, 0),
	(127, '5', 106, 'CORRECT', '0', '2026-06-26 04:31:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 5, 44.5, 100),
	(128, '5', 71, 'CORRECT', '1', '2026-06-26 04:33:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 6, 61.1, 100),
	(129, '5', 36, 'INCORRECT', '1', '2026-06-26 04:35:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 7, 71.8, 0),
	(132, '5', 105, 'CORRECT', '0', '2026-06-26 04:41:49.178083', 'abf1c635-119c-4b53-b25c-e11cabbe999a', 10, 42.3, 100),
	(133, '5', 31, 'CORRECT', '1', '2026-06-27 04:23:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 1, 55.5, 100),
	(134, '5', 245, 'INCORRECT', '1', '2026-06-27 04:25:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 2, 48.4, 0),
	(135, '5', 216, 'CORRECT', '0', '2026-06-27 04:27:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 3, 85.9, 100),
	(136, '5', 79, 'INCORRECT', '0', '2026-06-27 04:29:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 4, 89.1, 0),
	(137, '5', 134, 'INCORRECT', '2', '2026-06-27 04:31:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 5, 69.8, 0),
	(140, '5', 97, 'CORRECT', '0', '2026-06-27 04:37:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 8, 85.8, 100),
	(141, '5', 35, 'CORRECT', '2', '2026-06-27 04:39:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 9, 53.9, 100),
	(142, '5', 43, 'CORRECT', '2', '2026-06-27 04:41:49.178083', '142772bf-90b3-41d5-b1b5-3fb73be452b0', 10, 46.7, 100),
	(143, '5', 80, 'CORRECT', '3', '2026-06-28 04:23:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 1, 55, 100),
	(144, '5', 27, 'CORRECT', '1', '2026-06-28 04:25:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 2, 76.3, 100),
	(145, '5', 18, 'CORRECT', '1', '2026-06-28 04:27:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 3, 71.6, 100),
	(146, '5', 103, 'INCORRECT', '2', '2026-06-28 04:29:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 4, 62.1, 0),
	(147, '5', 45, 'INCORRECT', '1', '2026-06-28 04:31:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 5, 55.6, 0),
	(148, '5', 65, 'CORRECT', '0', '2026-06-28 04:33:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 6, 43.1, 100),
	(149, '5', 47, 'CORRECT', '3', '2026-06-28 04:35:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 7, 42.4, 100),
	(150, '5', 33, 'CORRECT', '0', '2026-06-28 04:37:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 8, 107.4, 100),
	(151, '5', 76, 'CORRECT', '1', '2026-06-28 04:39:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 9, 50.5, 100),
	(152, '5', 74, 'CORRECT', '1', '2026-06-28 04:41:49.178083', '51d5976b-c979-4288-8bd7-96daa2aa4836', 10, 44.9, 100),
	(153, '6', 43, 'CORRECT', '2', '2026-07-11 04:23:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 1, 33.5, 100),
	(154, '6', 196, 'CORRECT', '0', '2026-07-11 04:25:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 2, 43.9, 100),
	(155, '6', 241, 'CORRECT', '0', '2026-07-11 04:27:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 3, 33.9, 100),
	(156, '6', 78, 'CORRECT', '0', '2026-07-11 04:29:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 4, 37, 100),
	(157, '6', 11, 'INCORRECT', '3', '2026-07-11 04:31:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 5, 75.6, 0),
	(158, '6', 26, 'CORRECT', '1', '2026-07-11 04:33:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 6, 43.2, 100),
	(159, '6', 112, 'CORRECT', '1', '2026-07-11 04:35:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 7, 66.2, 100),
	(161, '6', 10, 'CORRECT', '1', '2026-07-11 04:39:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 9, 76.4, 100),
	(162, '6', 77, 'INCORRECT', '1', '2026-07-11 04:41:49.455531', '971ac233-89fb-4358-85e3-76e8f1013374', 10, 73.2, 0),
	(163, '6', 95, 'INCORRECT', '2', '2026-07-12 04:23:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 1, 71.9, 0),
	(164, '6', 23, 'CORRECT', '2', '2026-07-12 04:25:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 2, 96.4, 100),
	(165, '6', 48, 'INCORRECT', '2', '2026-07-12 04:27:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 3, 62.3, 0),
	(166, '6', 47, 'INCORRECT', '0', '2026-07-12 04:29:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 4, 62.9, 0),
	(167, '6', 51, 'CORRECT', '2', '2026-07-12 04:31:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 5, 57, 100),
	(168, '6', 71, 'CORRECT', '1', '2026-07-12 04:33:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 6, 54, 100),
	(169, '6', 32, 'CORRECT', '1', '2026-07-12 04:35:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 7, 55.3, 100),
	(170, '6', 272, 'INCORRECT', '2', '2026-07-12 04:37:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 8, 23.7, 0),
	(171, '6', 70, 'CORRECT', '3', '2026-07-12 04:39:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 9, 37.7, 100),
	(172, '6', 68, 'SKIP', NULL, '2026-07-12 04:41:49.455531', '7fa40372-7716-4e3e-b884-699ef3004763', 10, 97.8, 0),
	(174, '6', 45, 'INCORRECT', '1', '2026-07-13 04:25:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 2, 52.3, 0),
	(175, '6', 41, 'CORRECT', '1', '2026-07-13 04:27:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 3, 62.7, 100),
	(176, '6', 56, 'CORRECT', '1', '2026-07-13 04:29:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 4, 60.1, 100),
	(177, '6', 247, 'CORRECT', '0', '2026-07-13 04:31:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 5, 65.9, 100),
	(178, '6', 16, 'INCORRECT', '2', '2026-07-13 04:33:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 6, 11.7, 0),
	(179, '6', 259, 'CORRECT', '0', '2026-07-13 04:35:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 7, 99.1, 100),
	(180, '6', 74, 'INCORRECT', '0', '2026-07-13 04:37:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 8, 28.9, 0),
	(181, '6', 34, 'CORRECT', '0', '2026-07-13 04:39:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 9, 91.2, 100),
	(182, '6', 206, 'CORRECT', '0', '2026-07-13 04:41:49.455531', '5b5904a2-0152-42b1-97ed-36554b8a16b0', 10, 58.4, 100),
	(183, '6', 75, 'INCORRECT', '3', '2026-07-14 04:23:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 1, 55.4, 0),
	(184, '6', 114, 'INCORRECT', '0', '2026-07-14 04:25:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 2, 95.3, 0),
	(185, '6', 107, 'INCORRECT', '2', '2026-07-14 04:27:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 3, 77.6, 0),
	(186, '6', 97, 'CORRECT', '0', '2026-07-14 04:29:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 4, 82.5, 100),
	(187, '6', 225, 'CORRECT', '0', '2026-07-14 04:31:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 5, 76.7, 100),
	(188, '6', 90, 'CORRECT', '0', '2026-07-14 04:33:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 6, 81.2, 100),
	(189, '6', 187, 'CORRECT', '0', '2026-07-14 04:35:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 7, 56.4, 100),
	(191, '6', 13, 'CORRECT', '0', '2026-07-14 04:39:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 9, 86.6, 100),
	(192, '6', 72, 'CORRECT', '1', '2026-07-14 04:41:49.455531', '25887c15-636b-48df-bfad-631087f9bdea', 10, 41.8, 100),
	(193, '6', 243, 'CORRECT', '0', '2026-07-15 04:23:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 1, 63.3, 100),
	(194, '6', 30, 'INCORRECT', '3', '2026-07-15 04:25:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 2, 77, 0),
	(195, '6', 248, 'CORRECT', '0', '2026-07-15 04:27:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 3, 73.6, 100),
	(196, '6', 24, 'CORRECT', '0', '2026-07-15 04:29:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 4, 46.9, 100),
	(197, '6', 42, 'CORRECT', '1', '2026-07-15 04:31:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 5, 68.5, 100),
	(198, '6', 67, 'CORRECT', '0', '2026-07-15 04:33:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 6, 17.3, 100),
	(199, '6', 14, 'CORRECT', '1', '2026-07-15 04:35:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 7, 52.3, 100),
	(201, '6', 61, 'CORRECT', '1', '2026-07-15 04:39:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 9, 80.1, 100),
	(202, '6', 20, 'INCORRECT', '0', '2026-07-15 04:41:49.455531', '35774bf9-987c-41eb-af77-0059b37acfb4', 10, 54.6, 0),
	(203, '6', 27, 'CORRECT', '1', '2026-07-16 04:23:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 1, 45.7, 100),
	(204, '6', 149, 'CORRECT', '0', '2026-07-16 04:25:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 2, 89.6, 100),
	(205, '6', 35, 'CORRECT', '2', '2026-07-16 04:27:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 3, 72.2, 100),
	(206, '6', 257, 'CORRECT', '3', '2026-07-16 04:29:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 4, 108.6, 100),
	(207, '6', 63, 'CORRECT', '2', '2026-07-16 04:31:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 5, 55.2, 100),
	(208, '6', 22, 'CORRECT', '0', '2026-07-16 04:33:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 6, 92.8, 100),
	(209, '6', 21, 'CORRECT', '1', '2026-07-16 04:35:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 7, 63.3, 100),
	(210, '6', 46, 'INCORRECT', '2', '2026-07-16 04:37:49.455531', '40a75e2d-8068-4792-a183-df895c954cef', 8, 37.1, 0),
	(211, '7', 50, 'CORRECT', '2', '2026-06-21 04:23:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 1, 65.8, 100),
	(212, '7', 70, 'CORRECT', '3', '2026-06-21 04:25:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 2, 14, 100),
	(213, '7', 247, 'INCORRECT', '3', '2026-06-21 04:27:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 3, 76.8, 0),
	(214, '7', 275, 'CORRECT', '1', '2026-06-21 04:29:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 4, 69.7, 100),
	(215, '7', 176, 'CORRECT', '0', '2026-06-21 04:31:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 5, 60.1, 100),
	(216, '7', 218, 'CORRECT', '0', '2026-06-21 04:33:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 6, 66.4, 100),
	(217, '7', 242, 'INCORRECT', '3', '2026-06-21 04:35:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 7, 62.8, 0);
INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(218, '7', 134, 'INCORRECT', '3', '2026-06-21 04:37:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 8, 75.1, 0),
	(219, '7', 156, 'CORRECT', '0', '2026-06-21 04:39:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 9, 45.9, 100),
	(220, '7', 67, 'CORRECT', '0', '2026-06-21 04:41:49.725771', '6e5b10fd-2a1a-41aa-bd47-9f406a4ce32d', 10, 73.3, 100),
	(221, '7', 157, 'CORRECT', '0', '2026-06-22 04:23:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 1, 38.9, 100),
	(222, '7', 66, 'CORRECT', '0', '2026-06-22 04:25:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 2, 38.1, 100),
	(223, '7', 181, 'INCORRECT', '2', '2026-06-22 04:27:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 3, 72.4, 0),
	(224, '7', 113, 'CORRECT', '1', '2026-06-22 04:29:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 4, 52.9, 100),
	(225, '7', 78, 'INCORRECT', '1', '2026-06-22 04:31:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 5, 84, 0),
	(227, '7', 91, 'CORRECT', '1', '2026-06-22 04:35:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 7, 51.7, 100),
	(228, '7', 24, 'CORRECT', '0', '2026-06-22 04:37:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 8, 67.2, 100),
	(229, '7', 19, 'INCORRECT', '3', '2026-06-22 04:39:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 9, 67.7, 0),
	(230, '7', 58, 'CORRECT', '2', '2026-06-22 04:41:49.725771', '595b812a-d520-43e9-bed4-0e4b5625c3a4', 10, 68, 100),
	(231, '7', 93, 'CORRECT', '1', '2026-06-23 04:23:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 1, 55.1, 100),
	(232, '7', 246, 'CORRECT', '0', '2026-06-23 04:25:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 2, 42.9, 100),
	(233, '7', 80, 'CORRECT', '3', '2026-06-23 04:27:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 3, 45, 100),
	(234, '7', 79, 'INCORRECT', '0', '2026-06-23 04:29:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 4, 87.2, 0),
	(235, '7', 29, 'CORRECT', '1', '2026-06-23 04:31:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 5, 54.7, 100),
	(236, '7', 38, 'CORRECT', '1', '2026-06-23 04:33:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 6, 64.2, 100),
	(237, '7', 14, 'CORRECT', '1', '2026-06-23 04:35:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 7, 71.6, 100),
	(238, '7', 40, 'CORRECT', '2', '2026-06-23 04:37:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 8, 42, 100),
	(239, '7', 92, 'INCORRECT', '2', '2026-06-23 04:39:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 9, 69.1, 0),
	(240, '7', 227, 'SKIP', NULL, '2026-06-23 04:41:49.725771', 'd6bb7213-8e5f-4732-a149-e361b15e2c79', 10, 91.1, 0),
	(241, '7', 54, 'INCORRECT', '0', '2026-06-24 04:23:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 1, 66.5, 0),
	(243, '7', 37, 'CORRECT', '1', '2026-06-24 04:27:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 3, 75.9, 100),
	(244, '7', 52, 'CORRECT', '1', '2026-06-24 04:29:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 4, 62.5, 100),
	(245, '7', 68, 'CORRECT', '2', '2026-06-24 04:31:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 5, 79, 100),
	(246, '7', 57, 'CORRECT', '1', '2026-06-24 04:33:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 6, 58.1, 100),
	(248, '7', 123, 'CORRECT', '0', '2026-06-24 04:37:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 8, 57.2, 100),
	(249, '7', 255, 'INCORRECT', '2', '2026-06-24 04:39:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 9, 59.8, 0),
	(250, '7', 42, 'SKIP', NULL, '2026-06-24 04:41:49.725771', '39396972-498d-47c0-8ac6-207077a6027a', 10, 69.5, 0),
	(251, '7', 65, 'CORRECT', '0', '2026-06-25 04:23:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 1, 75.3, 100),
	(252, '7', 43, 'INCORRECT', '0', '2026-06-25 04:25:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 2, 78.5, 0),
	(253, '7', 30, 'CORRECT', '0', '2026-06-25 04:27:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 3, 69.9, 100),
	(254, '7', 63, 'INCORRECT', '0', '2026-06-25 04:29:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 4, 61.6, 0),
	(255, '7', 162, 'INCORRECT', '1', '2026-06-25 04:31:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 5, 32.1, 0),
	(256, '7', 89, 'INCORRECT', '2', '2026-06-25 04:33:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 6, 49.9, 0),
	(257, '7', 121, 'CORRECT', '0', '2026-06-25 04:35:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 7, 52.3, 100),
	(258, '7', 27, 'CORRECT', '1', '2026-06-25 04:37:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 8, 46.5, 100),
	(259, '7', 267, 'INCORRECT', '1', '2026-06-25 04:39:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 9, 57.4, 0),
	(260, '7', 184, 'INCORRECT', '2', '2026-06-25 04:41:49.725771', 'ac33459f-3307-4008-9ac4-8d130686564f', 10, 43.1, 0),
	(262, '7', 124, 'INCORRECT', '1', '2026-06-26 04:25:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 2, 40.6, 0),
	(263, '7', 23, 'INCORRECT', '1', '2026-06-26 04:27:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 3, 98.4, 0),
	(264, '7', 34, 'CORRECT', '0', '2026-06-26 04:29:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 4, 67.1, 100),
	(265, '7', 36, 'CORRECT', '2', '2026-06-26 04:31:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 5, 100.8, 100),
	(266, '7', 31, 'CORRECT', '1', '2026-06-26 04:33:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 6, 40.4, 100),
	(267, '7', 237, 'CORRECT', '0', '2026-06-26 04:35:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 7, 42.3, 100),
	(268, '7', 174, 'CORRECT', '0', '2026-06-26 04:37:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 8, 51.7, 100),
	(269, '7', 76, 'INCORRECT', '2', '2026-06-26 04:39:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 9, 64.1, 0),
	(270, '7', 17, 'CORRECT', '2', '2026-06-26 04:41:49.725771', '7d215071-2247-4c4d-b4be-d034b28975dc', 10, 50, 100),
	(271, '7', 74, 'CORRECT', '1', '2026-06-27 04:23:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 1, 69.2, 100),
	(272, '7', 141, 'INCORRECT', '3', '2026-06-27 04:25:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 2, 51.1, 0),
	(273, '7', 71, 'CORRECT', '1', '2026-06-27 04:27:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 3, 64.9, 100),
	(274, '7', 147, 'INCORRECT', '1', '2026-06-27 04:29:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 4, 73.3, 0),
	(275, '7', 144, 'CORRECT', '0', '2026-06-27 04:31:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 5, 37.3, 100),
	(276, '7', 62, 'INCORRECT', '3', '2026-06-27 04:33:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 6, 38.5, 0),
	(277, '7', 49, 'CORRECT', '1', '2026-06-27 04:35:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 7, 38.4, 100),
	(278, '7', 55, 'CORRECT', '1', '2026-06-27 04:37:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 8, 53.1, 100),
	(279, '7', 45, 'CORRECT', '0', '2026-06-27 04:39:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 9, 34.9, 100),
	(280, '7', 99, 'CORRECT', '0', '2026-06-27 04:41:49.725771', '48170fe0-4c6b-4a87-9558-b0d9cdadb667', 10, 56.3, 100),
	(281, '7', 215, 'INCORRECT', '2', '2026-06-28 04:23:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 1, 113.4, 0),
	(282, '7', 69, 'CORRECT', '0', '2026-06-28 04:25:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 2, 86.5, 100),
	(283, '7', 32, 'CORRECT', '1', '2026-06-28 04:27:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 3, 79.2, 100),
	(284, '7', 117, 'INCORRECT', '2', '2026-06-28 04:29:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 4, 65.5, 0),
	(285, '7', 16, 'INCORRECT', '0', '2026-06-28 04:31:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 5, 58.1, 0),
	(286, '7', 274, 'CORRECT', '3', '2026-06-28 04:33:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 6, 71.1, 100),
	(287, '7', 105, 'INCORRECT', '2', '2026-06-28 04:35:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 7, 39.3, 0),
	(288, '7', 196, 'CORRECT', '0', '2026-06-28 04:37:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 8, 83.3, 100),
	(289, '7', 182, 'CORRECT', '3', '2026-06-28 04:39:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 9, 75.9, 100),
	(290, '7', 15, 'CORRECT', '3', '2026-06-28 04:41:49.725771', '1b41f244-e506-4278-a50f-940ac8c3e1b9', 10, 79.4, 100),
	(291, '7', 33, 'INCORRECT', '1', '2026-06-29 04:23:49.725771', '0b624a7f-5031-425d-a800-e599fa0b6af0', 1, 83.4, 0),
	(292, '8', 44, 'CORRECT', '1', '2026-06-25 04:23:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 1, 76.1, 100),
	(293, '8', 67, 'INCORRECT', '2', '2026-06-25 04:25:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 2, 37.7, 0),
	(294, '8', 60, 'CORRECT', '0', '2026-06-25 04:27:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 3, 56.4, 100),
	(295, '8', 27, 'CORRECT', '1', '2026-06-25 04:29:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 4, 69.1, 100),
	(296, '8', 72, 'INCORRECT', '3', '2026-06-25 04:31:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 5, 45.6, 0),
	(297, '8', 26, 'INCORRECT', '2', '2026-06-25 04:33:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 6, 28.3, 0),
	(298, '8', 18, 'CORRECT', '1', '2026-06-25 04:35:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 7, 79.5, 100),
	(299, '8', 13, 'INCORRECT', '3', '2026-06-25 04:37:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 8, 40.2, 0),
	(300, '8', 108, 'CORRECT', '1', '2026-06-25 04:39:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 9, 53.4, 100),
	(301, '8', 183, 'CORRECT', '0', '2026-06-25 04:41:50.004229', '5bb3bee5-c69a-408d-a449-e83d3962d527', 10, 59.3, 100),
	(302, '8', 52, 'CORRECT', '1', '2026-06-26 04:23:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 1, 26.6, 100),
	(303, '8', 10, 'INCORRECT', '0', '2026-06-26 04:25:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 2, 42.1, 0),
	(304, '8', 212, 'CORRECT', '0', '2026-06-26 04:27:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 3, 62.3, 100),
	(305, '8', 73, 'INCORRECT', '0', '2026-06-26 04:29:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 4, 76.9, 0),
	(306, '8', 71, 'INCORRECT', '0', '2026-06-26 04:31:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 5, 56.2, 0),
	(307, '8', 54, 'CORRECT', '2', '2026-06-26 04:33:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 6, 98.4, 100),
	(308, '8', 41, 'INCORRECT', '0', '2026-06-26 04:35:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 7, 78.8, 0),
	(309, '8', 50, 'CORRECT', '2', '2026-06-26 04:37:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 8, 48.4, 100),
	(310, '8', 78, 'INCORRECT', '1', '2026-06-26 04:39:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 9, 42.5, 0),
	(311, '8', 40, 'CORRECT', '2', '2026-06-26 04:41:50.004229', 'c708259d-30ed-4cbb-bfee-4c7469d8c95b', 10, 55.9, 100),
	(313, '8', 63, 'CORRECT', '2', '2026-06-27 04:25:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 2, 70.2, 100),
	(314, '8', 97, 'INCORRECT', '3', '2026-06-27 04:27:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 3, 76.6, 0),
	(315, '8', 12, 'INCORRECT', '1', '2026-06-27 04:29:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 4, 46.4, 0),
	(316, '8', 233, 'CORRECT', '0', '2026-06-27 04:31:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 5, 30.5, 100),
	(317, '8', 93, 'CORRECT', '1', '2026-06-27 04:33:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 6, 34.7, 100),
	(319, '8', 31, 'CORRECT', '1', '2026-06-27 04:37:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 8, 70.9, 100),
	(320, '8', 62, 'CORRECT', '0', '2026-06-27 04:39:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 9, 52.8, 100),
	(321, '8', 134, 'INCORRECT', '1', '2026-06-27 04:41:50.004229', '838ea203-5965-4503-8b7c-3a1526aff1cc', 10, 91.5, 0),
	(322, '8', 14, 'CORRECT', '1', '2026-06-28 04:23:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 1, 56.2, 100),
	(323, '8', 39, 'CORRECT', '1', '2026-06-28 04:25:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 2, 70, 100);
INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(324, '8', 25, 'CORRECT', '3', '2026-06-28 04:27:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 3, 29.7, 100),
	(325, '8', 77, 'CORRECT', '0', '2026-06-28 04:29:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 4, 42.7, 100),
	(326, '8', 29, 'CORRECT', '1', '2026-06-28 04:31:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 5, 77.4, 100),
	(327, '8', 47, 'CORRECT', '3', '2026-06-28 04:33:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 6, 66.5, 100),
	(328, '8', 35, 'INCORRECT', '0', '2026-06-28 04:35:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 7, 87.5, 0),
	(329, '8', 247, 'INCORRECT', '2', '2026-06-28 04:37:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 8, 71.6, 0),
	(331, '8', 61, 'INCORRECT', '0', '2026-06-28 04:41:50.004229', 'c19c9f92-1f07-4602-9a81-8cb701bd47ba', 10, 29.1, 0),
	(332, '8', 176, 'CORRECT', '0', '2026-06-29 04:23:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 1, 49.2, 100),
	(333, '8', 124, 'INCORRECT', '3', '2026-06-29 04:25:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 2, 82.5, 0),
	(334, '8', 130, 'CORRECT', '0', '2026-06-29 04:27:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 3, 89.6, 100),
	(335, '8', 19, 'CORRECT', '2', '2026-06-29 04:29:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 4, 38.7, 100),
	(336, '8', 53, 'CORRECT', '0', '2026-06-29 04:31:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 5, 59.1, 100),
	(337, '8', 32, 'CORRECT', '1', '2026-06-29 04:33:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 6, 28.6, 100),
	(338, '8', 195, 'CORRECT', '0', '2026-06-29 04:35:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 7, 49.4, 100),
	(339, '8', 76, 'CORRECT', '1', '2026-06-29 04:37:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 8, 85.1, 100),
	(340, '8', 80, 'INCORRECT', '0', '2026-06-29 04:39:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 9, 28.3, 0),
	(341, '8', 261, 'CORRECT', 'append()', '2026-06-29 04:41:50.004229', '232b2f64-7d3b-4e73-8d13-a0c9655587b4', 10, 51.5, 100),
	(342, '8', 42, 'CORRECT', '1', '2026-06-30 04:23:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 1, 54.9, 100),
	(344, '8', 11, 'CORRECT', '1', '2026-06-30 04:27:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 3, 78.1, 100),
	(345, '8', 64, 'INCORRECT', '0', '2026-06-30 04:29:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 4, 49.9, 0),
	(346, '8', 65, 'SKIP', NULL, '2026-06-30 04:31:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 5, 81.6, 0),
	(347, '8', 149, 'INCORRECT', '2', '2026-06-30 04:33:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 6, 59.7, 0),
	(348, '8', 189, 'INCORRECT', '3', '2026-06-30 04:35:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 7, 51.7, 0),
	(349, '8', 258, 'CORRECT', '0', '2026-06-30 04:37:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 8, 55.5, 100),
	(350, '8', 164, 'CORRECT', '0', '2026-06-30 04:39:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 9, 83.8, 100),
	(351, '8', 75, 'CORRECT', '0', '2026-06-30 04:41:50.004229', '5728978a-3d63-41b8-b974-14cc01d7d27a', 10, 49.6, 100),
	(352, '8', 103, 'INCORRECT', '2', '2026-07-01 04:23:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 1, 87.7, 0),
	(353, '8', 112, 'CORRECT', '1', '2026-07-01 04:25:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 2, 66.4, 100),
	(354, '8', 36, 'CORRECT', '2', '2026-07-01 04:27:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 3, 99.3, 100),
	(355, '8', 70, 'CORRECT', '3', '2026-07-01 04:29:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 4, 20.6, 100),
	(356, '8', 66, 'CORRECT', '0', '2026-07-01 04:31:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 5, 63.9, 100),
	(357, '8', 33, 'INCORRECT', '3', '2026-07-01 04:33:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 6, 69.8, 0),
	(358, '8', 242, 'INCORRECT', '3', '2026-07-01 04:35:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 7, 64.1, 0),
	(359, '8', 23, 'INCORRECT', '3', '2026-07-01 04:37:50.004229', 'ae83a0ed-e76f-407d-aeac-628cb097cb71', 8, 81.6, 0),
	(360, '9', 115, 'INCORRECT', '1', '2026-07-01 04:23:50.277866', 'c3e483ff-feae-4181-ac67-4b4eb6f37818', 1, 86.5, 0),
	(361, '9', 19, 'CORRECT', '2', '2026-07-01 04:25:50.277866', 'c3e483ff-feae-4181-ac67-4b4eb6f37818', 2, 28, 100),
	(364, '9', 33, 'INCORRECT', '2', '2026-07-01 04:31:50.277866', 'c3e483ff-feae-4181-ac67-4b4eb6f37818', 5, 47.9, 0),
	(365, '9', 20, 'INCORRECT', '1', '2026-07-01 04:33:50.277866', 'c3e483ff-feae-4181-ac67-4b4eb6f37818', 6, 67.2, 0),
	(367, '9', 229, 'CORRECT', '0', '2026-07-01 04:37:50.277866', 'c3e483ff-feae-4181-ac67-4b4eb6f37818', 8, 85.4, 100),
	(368, '9', 10, 'CORRECT', '1', '2026-07-01 04:39:50.277866', 'c3e483ff-feae-4181-ac67-4b4eb6f37818', 9, 31.7, 100),
	(369, '9', 138, 'CORRECT', '0', '2026-07-01 04:41:50.277866', 'c3e483ff-feae-4181-ac67-4b4eb6f37818', 10, 43.4, 100),
	(370, '9', 78, 'SKIP', NULL, '2026-07-02 04:23:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 1, 77.2, 0),
	(371, '9', 74, 'CORRECT', '1', '2026-07-02 04:25:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 2, 48.9, 100),
	(372, '9', 64, 'CORRECT', '2', '2026-07-02 04:27:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 3, 89.7, 100),
	(373, '9', 226, 'CORRECT', '0', '2026-07-02 04:29:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 4, 36.3, 100),
	(374, '9', 50, 'CORRECT', '2', '2026-07-02 04:31:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 5, 63.8, 100),
	(375, '9', 68, 'INCORRECT', '3', '2026-07-02 04:33:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 6, 92.1, 0),
	(376, '9', 70, 'CORRECT', '3', '2026-07-02 04:35:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 7, 63.3, 100),
	(377, '9', 49, 'INCORRECT', '2', '2026-07-02 04:37:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 8, 39.5, 0),
	(378, '9', 13, 'INCORRECT', '3', '2026-07-02 04:39:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 9, 50.3, 0),
	(379, '9', 91, 'CORRECT', '1', '2026-07-02 04:41:50.277866', '6687b44b-6cd2-456e-84b9-24fe4fedc423', 10, 60.3, 100),
	(381, '9', 22, 'CORRECT', '0', '2026-07-03 04:25:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 2, 46.3, 100),
	(382, '9', 250, 'INCORRECT', '1', '2026-07-03 04:27:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 3, 77.4, 0),
	(383, '9', 214, 'CORRECT', '0', '2026-07-03 04:29:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 4, 47.6, 100),
	(384, '9', 58, 'CORRECT', '2', '2026-07-03 04:31:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 5, 81.5, 100),
	(385, '9', 44, 'CORRECT', '1', '2026-07-03 04:33:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 6, 58.5, 100),
	(386, '9', 39, 'INCORRECT', '2', '2026-07-03 04:35:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 7, 68.8, 0),
	(387, '9', 62, 'CORRECT', '0', '2026-07-03 04:37:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 8, 47.3, 100),
	(388, '9', 16, 'CORRECT', '1', '2026-07-03 04:39:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 9, 19.6, 100),
	(389, '9', 24, 'INCORRECT', '3', '2026-07-03 04:41:50.277866', '86c4e780-4a1a-4041-8ab5-18c499d39eb8', 10, 44.7, 0),
	(390, '9', 66, 'INCORRECT', '1', '2026-07-04 04:23:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 1, 61.7, 0),
	(391, '9', 263, 'CORRECT', 'total = 0

for i in range(1, 11):
    total += i

print(total)', '2026-07-04 04:25:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 2, 20.7, 100),
	(392, '9', 17, 'CORRECT', '2', '2026-07-04 04:27:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 3, 71.4, 100),
	(393, '9', 197, 'INCORRECT', '1', '2026-07-04 04:29:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 4, 69.8, 0),
	(394, '9', 38, 'INCORRECT', '0', '2026-07-04 04:31:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 5, 55.5, 0),
	(395, '9', 150, 'INCORRECT', '3', '2026-07-04 04:33:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 6, 45.4, 0),
	(396, '9', 87, 'CORRECT', '0', '2026-07-04 04:35:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 7, 69, 100),
	(397, '9', 40, 'INCORRECT', '0', '2026-07-04 04:37:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 8, 28.3, 0),
	(398, '9', 111, 'INCORRECT', '2', '2026-07-04 04:39:50.277866', '044c19a4-44f5-4af2-8d17-3c573e928a84', 9, 54.6, 0),
	(400, '9', 55, 'INCORRECT', '2', '2026-07-05 04:23:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 1, 91.2, 0),
	(401, '9', 185, 'CORRECT', '0', '2026-07-05 04:25:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 2, 47.1, 100),
	(402, '9', 42, 'INCORRECT', '0', '2026-07-05 04:27:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 3, 68.9, 0),
	(403, '9', 80, 'INCORRECT', '2', '2026-07-05 04:29:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 4, 46.5, 0),
	(404, '9', 37, 'CORRECT', '1', '2026-07-05 04:31:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 5, 92.1, 100),
	(405, '9', 41, 'INCORRECT', '2', '2026-07-05 04:33:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 6, 96.8, 0),
	(406, '9', 243, 'CORRECT', '0', '2026-07-05 04:35:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 7, 49.6, 100),
	(407, '9', 21, 'INCORRECT', '2', '2026-07-05 04:37:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 8, 90.6, 0),
	(408, '9', 27, 'INCORRECT', '2', '2026-07-05 04:39:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 9, 67.6, 0),
	(409, '9', 59, 'INCORRECT', '0', '2026-07-05 04:41:50.277866', 'eae3b4a5-5f3b-4a03-bb73-c602e792da96', 10, 98, 0),
	(410, '9', 28, 'CORRECT', '0', '2026-07-06 04:23:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 1, 59.3, 100),
	(411, '9', 63, 'CORRECT', '2', '2026-07-06 04:25:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 2, 64.8, 100),
	(412, '9', 71, 'INCORRECT', '3', '2026-07-06 04:27:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 3, 20.8, 0),
	(414, '9', 36, 'INCORRECT', '0', '2026-07-06 04:31:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 5, 60.6, 0),
	(415, '9', 213, 'INCORRECT', '3', '2026-07-06 04:33:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 6, 67.9, 0),
	(416, '9', 51, 'CORRECT', '2', '2026-07-06 04:35:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 7, 36.7, 100),
	(417, '9', 18, 'CORRECT', '1', '2026-07-06 04:37:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 8, 65.2, 100),
	(418, '9', 48, 'CORRECT', '1', '2026-07-06 04:39:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 9, 65.8, 100),
	(419, '9', 95, 'INCORRECT', '3', '2026-07-06 04:41:50.277866', '1c0ca879-edd4-4e89-9621-478a2bdeeb95', 10, 87.4, 0),
	(420, '10', 255, 'INCORRECT', '3', '2026-06-22 04:23:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 1, 8, 0),
	(422, '10', 131, 'CORRECT', '0', '2026-06-22 04:27:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 3, 16.1, 100),
	(423, '10', 140, 'INCORRECT', '1', '2026-06-22 04:29:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 4, 44.9, 0),
	(424, '10', 10, 'INCORRECT', '0', '2026-06-22 04:31:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 5, 55.9, 0),
	(426, '10', 259, 'CORRECT', '0', '2026-06-22 04:35:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 7, 78.5, 100),
	(427, '10', 62, 'INCORRECT', '1', '2026-06-22 04:37:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 8, 19.1, 0),
	(428, '10', 95, 'CORRECT', '1', '2026-06-22 04:39:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 9, 51.9, 100),
	(429, '10', 127, 'CORRECT', '0', '2026-06-22 04:41:50.566609', '17b58ef7-8dc2-4fce-87f2-d6f361b1e366', 10, 93.8, 100),
	(430, '10', 18, 'INCORRECT', '0', '2026-06-23 04:23:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 1, 62.3, 0),
	(431, '10', 14, 'INCORRECT', '0', '2026-06-23 04:25:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 2, 25, 0),
	(432, '10', 87, 'INCORRECT', '2', '2026-06-23 04:27:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 3, 57, 0),
	(433, '10', 36, 'CORRECT', '2', '2026-06-23 04:29:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 4, 80.7, 100);
INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(434, '10', 184, 'CORRECT', '0', '2026-06-23 04:31:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 5, 33.1, 100),
	(435, '10', 237, 'CORRECT', '0', '2026-06-23 04:33:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 6, 27, 100),
	(436, '10', 41, 'CORRECT', '1', '2026-06-23 04:35:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 7, 73.1, 100),
	(437, '10', 44, 'CORRECT', '1', '2026-06-23 04:37:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 8, 77.7, 100),
	(438, '10', 59, 'CORRECT', '1', '2026-06-23 04:39:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 9, 86.6, 100),
	(439, '10', 46, 'CORRECT', '1', '2026-06-23 04:41:50.566609', '67c6db24-b249-469e-82ec-b8cdaa009c68', 10, 94.4, 100),
	(440, '10', 25, 'INCORRECT', '2', '2026-06-24 04:23:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 1, 53.9, 0),
	(442, '10', 161, 'INCORRECT', '2', '2026-06-24 04:27:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 3, 75.8, 0),
	(443, '10', 17, 'INCORRECT', '1', '2026-06-24 04:29:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 4, 62.4, 0),
	(444, '10', 42, 'INCORRECT', '2', '2026-06-24 04:31:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 5, 56.7, 0),
	(445, '10', 80, 'CORRECT', '3', '2026-06-24 04:33:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 6, 81, 100),
	(447, '10', 57, 'CORRECT', '1', '2026-06-24 04:37:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 8, 64.3, 100),
	(448, '10', 155, 'CORRECT', '0', '2026-06-24 04:39:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 9, 46.6, 100),
	(449, '10', 234, 'INCORRECT', '3', '2026-06-24 04:41:50.566609', 'e417fa95-3925-4e2d-9ab8-d3ed0ab1a02b', 10, 50, 0),
	(451, '10', 48, 'INCORRECT', '2', '2026-06-25 04:25:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 2, 93.2, 0),
	(452, '10', 43, 'INCORRECT', '0', '2026-06-25 04:27:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 3, 94.5, 0),
	(453, '10', 222, 'CORRECT', '0', '2026-06-25 04:29:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 4, 56.1, 100),
	(454, '10', 58, 'INCORRECT', '1', '2026-06-25 04:31:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 5, 76.8, 0),
	(455, '10', 71, 'INCORRECT', '2', '2026-06-25 04:33:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 6, 50.4, 0),
	(456, '10', 79, 'INCORRECT', '3', '2026-06-25 04:35:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 7, 52.6, 0),
	(457, '10', 224, 'CORRECT', '0', '2026-06-25 04:37:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 8, 63.2, 100),
	(458, '10', 53, 'CORRECT', '0', '2026-06-25 04:39:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 9, 88.6, 100),
	(459, '10', 16, 'CORRECT', '1', '2026-06-25 04:41:50.566609', '2965e48a-d30b-45c5-b440-5df6377439df', 10, 45.5, 100),
	(460, '10', 165, 'CORRECT', '0', '2026-06-26 04:23:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 1, 43.4, 100),
	(461, '10', 158, 'INCORRECT', '1', '2026-06-26 04:25:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 2, 8, 0),
	(462, '10', 98, 'INCORRECT', '2', '2026-06-26 04:27:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 3, 73.9, 0),
	(463, '10', 99, 'INCORRECT', '1', '2026-06-26 04:29:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 4, 54.3, 0),
	(464, '10', 144, 'INCORRECT', '3', '2026-06-26 04:31:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 5, 77.4, 0),
	(465, '10', 73, 'CORRECT', '2', '2026-06-26 04:33:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 6, 90.3, 100),
	(466, '10', 24, 'CORRECT', '0', '2026-06-26 04:35:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 7, 79, 100),
	(467, '10', 19, 'CORRECT', '2', '2026-06-26 04:37:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 8, 57, 100),
	(468, '10', 120, 'INCORRECT', '0', '2026-06-26 04:39:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 9, 58.6, 0),
	(469, '10', 32, 'INCORRECT', '2', '2026-06-26 04:41:50.566609', '4e3e78b5-0ab7-4048-a9d4-917da1ba9633', 10, 42, 0),
	(470, '10', 64, 'INCORRECT', '0', '2026-06-27 04:23:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 1, 60.9, 0),
	(471, '10', 219, 'CORRECT', '0', '2026-06-27 04:25:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 2, 32.2, 100),
	(472, '10', 30, 'INCORRECT', '1', '2026-06-27 04:27:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 3, 48, 0),
	(473, '10', 34, 'INCORRECT', '1', '2026-06-27 04:29:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 4, 42.5, 0),
	(474, '10', 74, 'INCORRECT', '2', '2026-06-27 04:31:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 5, 67, 0),
	(475, '10', 211, 'CORRECT', '0', '2026-06-27 04:33:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 6, 51.1, 100),
	(476, '10', 271, 'INCORRECT', '3', '2026-06-27 04:35:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 7, 60.5, 0),
	(477, '10', 185, 'CORRECT', '0', '2026-06-27 04:37:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 8, 66.2, 100),
	(478, '10', 40, 'CORRECT', '2', '2026-06-27 04:39:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 9, 85.4, 100),
	(479, '10', 45, 'INCORRECT', '1', '2026-06-27 04:41:50.566609', '2149eb46-fa12-48d1-a071-24acfe8d6bc6', 10, 53, 0),
	(480, '10', 65, 'INCORRECT', '1', '2026-06-28 04:23:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 1, 52.8, 0),
	(481, '10', 54, 'INCORRECT', '1', '2026-06-28 04:25:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 2, 109.8, 0),
	(482, '10', 111, 'CORRECT', '0', '2026-06-28 04:27:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 3, 55.5, 100),
	(483, '10', 31, 'INCORRECT', '2', '2026-06-28 04:29:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 4, 33.6, 0),
	(484, '10', 244, 'INCORRECT', '1', '2026-06-28 04:31:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 5, 42.2, 0),
	(485, '10', 248, 'INCORRECT', '2', '2026-06-28 04:33:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 6, 86.4, 0),
	(486, '10', 33, 'INCORRECT', '2', '2026-06-28 04:35:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 7, 71.3, 0),
	(487, '10', 28, 'INCORRECT', '2', '2026-06-28 04:37:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 8, 49.8, 0),
	(488, '10', 84, 'INCORRECT', '3', '2026-06-28 04:39:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 9, 68.2, 0),
	(489, '10', 37, 'INCORRECT', '2', '2026-06-28 04:41:50.566609', '0f6bc69e-fc13-4821-b9a4-7828b1423ddf', 10, 103.4, 0),
	(491, '10', 27, 'CORRECT', '1', '2026-06-29 04:25:50.566609', 'ec6b9009-b8dd-4233-bbc0-2374bc7b93ee', 2, 54.3, 100),
	(492, '10', 21, 'INCORRECT', '2', '2026-06-29 04:27:50.566609', 'ec6b9009-b8dd-4233-bbc0-2374bc7b93ee', 3, 47.1, 0),
	(493, '11', 67, 'INCORRECT', '2', '2026-07-13 04:23:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 1, 65.3, 0),
	(494, '11', 74, 'SKIP', NULL, '2026-07-13 04:25:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 2, 55.1, 0),
	(495, '11', 75, 'INCORRECT', '1', '2026-07-13 04:27:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 3, 15.6, 0),
	(496, '11', 65, 'INCORRECT', '3', '2026-07-13 04:29:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 4, 74.3, 0),
	(497, '11', 34, 'INCORRECT', '2', '2026-07-13 04:31:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 5, 47, 0),
	(498, '11', 109, 'INCORRECT', '3', '2026-07-13 04:33:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 6, 72.1, 0),
	(499, '11', 15, 'CORRECT', '3', '2026-07-13 04:35:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 7, 55.3, 100),
	(500, '11', 195, 'INCORRECT', '2', '2026-07-13 04:37:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 8, 64.2, 0),
	(501, '11', 230, 'INCORRECT', '2', '2026-07-13 04:39:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 9, 54.9, 0),
	(502, '11', 228, 'CORRECT', '0', '2026-07-13 04:41:50.856868', 'c646131e-c6ed-408b-ada0-97fb1a6f40f2', 10, 8, 100),
	(503, '11', 35, 'CORRECT', '2', '2026-07-14 04:23:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 1, 48, 100),
	(505, '11', 44, 'CORRECT', '1', '2026-07-14 04:27:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 3, 90.2, 100),
	(506, '11', 121, 'INCORRECT', '3', '2026-07-14 04:29:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 4, 23.2, 0),
	(507, '11', 193, 'INCORRECT', '1', '2026-07-14 04:31:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 5, 46, 0),
	(508, '11', 104, 'CORRECT', '0', '2026-07-14 04:33:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 6, 64.8, 100),
	(509, '11', 107, 'INCORRECT', '3', '2026-07-14 04:35:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 7, 69.2, 0),
	(511, '11', 69, 'INCORRECT', '2', '2026-07-14 04:39:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 9, 85.6, 0),
	(512, '11', 42, 'CORRECT', '1', '2026-07-14 04:41:50.856868', '0f6a7bcf-2806-4186-9423-9d39bf8fa2f9', 10, 37.4, 100),
	(513, '11', 240, 'CORRECT', '3', '2026-07-15 04:23:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 1, 39.8, 100),
	(515, '11', 55, 'INCORRECT', '2', '2026-07-15 04:27:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 3, 86.6, 0),
	(516, '11', 33, 'CORRECT', '0', '2026-07-15 04:29:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 4, 45.6, 100),
	(517, '11', 23, 'CORRECT', '2', '2026-07-15 04:31:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 5, 58.9, 100),
	(518, '11', 36, 'INCORRECT', '0', '2026-07-15 04:33:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 6, 89.5, 0),
	(519, '11', 73, 'INCORRECT', '0', '2026-07-15 04:35:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 7, 64.6, 0),
	(520, '11', 30, 'INCORRECT', '3', '2026-07-15 04:37:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 8, 38.7, 0),
	(521, '11', 43, 'INCORRECT', '1', '2026-07-15 04:39:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 9, 67.8, 0),
	(522, '11', 18, 'INCORRECT', '2', '2026-07-15 04:41:50.856868', '65585ff9-e02e-4f55-8fae-125a33375e3a', 10, 53.9, 0),
	(523, '11', 40, 'INCORRECT', '3', '2026-07-16 04:23:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 1, 55.6, 0),
	(525, '11', 25, 'INCORRECT', '1', '2026-07-16 04:27:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 3, 43.8, 0),
	(526, '11', 163, 'CORRECT', '0', '2026-07-16 04:29:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 4, 35.6, 100),
	(527, '11', 132, 'INCORRECT', '3', '2026-07-16 04:31:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 5, 65.7, 0),
	(528, '11', 149, 'INCORRECT', '1', '2026-07-16 04:33:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 6, 41.8, 0),
	(529, '11', 259, 'INCORRECT', '3', '2026-07-16 04:35:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 7, 53.9, 0),
	(530, '11', 21, 'INCORRECT', '2', '2026-07-16 04:37:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 8, 49.5, 0),
	(531, '11', 26, 'INCORRECT', '0', '2026-07-16 04:39:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 9, 69.8, 0),
	(532, '11', 198, 'CORRECT', '0', '2026-07-16 04:41:50.856868', 'b964139b-48f3-4612-b27e-ee5c55777e54', 10, 55, 100),
	(533, '11', 158, 'INCORRECT', '2', '2026-07-17 04:23:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 1, 84.4, 0),
	(534, '11', 24, 'INCORRECT', '2', '2026-07-17 04:25:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 2, 35.4, 0),
	(535, '11', 70, 'CORRECT', '3', '2026-07-17 04:27:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 3, 60.5, 100),
	(536, '11', 11, 'INCORRECT', '0', '2026-07-17 04:29:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 4, 47.9, 0),
	(537, '11', 176, 'CORRECT', '0', '2026-07-17 04:31:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 5, 93.2, 100),
	(538, '11', 252, 'INCORRECT', '1', '2026-07-17 04:33:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 6, 63.1, 0),
	(539, '11', 61, 'CORRECT', '1', '2026-07-17 04:35:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 7, 40.1, 100),
	(540, '11', 53, 'CORRECT', '0', '2026-07-17 04:37:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 8, 57.6, 100),
	(541, '11', 47, 'INCORRECT', '0', '2026-07-17 04:39:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 9, 58.5, 0);
INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(542, '11', 19, 'CORRECT', '2', '2026-07-17 04:41:50.856868', '1f21af38-376a-438d-badf-12e6cb078de1', 10, 58.5, 100),
	(544, '11', 86, 'INCORRECT', '2', '2026-07-18 04:25:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 2, 41.1, 0),
	(545, '11', 20, 'INCORRECT', '1', '2026-07-18 04:27:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 3, 61.2, 0),
	(546, '11', 48, 'INCORRECT', '0', '2026-07-18 04:29:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 4, 40.7, 0),
	(547, '11', 253, 'SKIP', NULL, '2026-07-18 04:31:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 5, 72.7, 0),
	(548, '11', 68, 'INCORRECT', '3', '2026-07-18 04:33:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 6, 66.8, 0),
	(549, '11', 31, 'INCORRECT', '0', '2026-07-18 04:35:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 7, 51.7, 0),
	(550, '11', 79, 'INCORRECT', '0', '2026-07-18 04:37:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 8, 77.7, 0),
	(551, '11', 76, 'CORRECT', '1', '2026-07-18 04:39:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 9, 97.8, 100),
	(552, '11', 28, 'CORRECT', '0', '2026-07-18 04:41:50.856868', '8db28499-6ff4-4709-adb1-269a14e476ae', 10, 48.3, 100),
	(553, '11', 16, 'CORRECT', '1', '2026-07-19 04:23:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 1, 53.8, 100),
	(554, '11', 87, 'INCORRECT', '2', '2026-07-19 04:25:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 2, 89.9, 0),
	(555, '11', 63, 'CORRECT', '2', '2026-07-19 04:27:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 3, 90.9, 100),
	(556, '11', 57, 'INCORRECT', '3', '2026-07-19 04:29:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 4, 79.4, 0),
	(557, '11', 233, 'CORRECT', '0', '2026-07-19 04:31:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 5, 85.5, 100),
	(558, '11', 128, 'CORRECT', '0', '2026-07-19 04:33:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 6, 45.8, 100),
	(559, '11', 13, 'INCORRECT', '2', '2026-07-19 04:35:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 7, 73.3, 0),
	(561, '11', 77, 'CORRECT', '0', '2026-07-19 04:39:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 9, 48.9, 100),
	(562, '11', 127, 'INCORRECT', '2', '2026-07-19 04:41:50.856868', 'c64b1a92-5590-43b6-a527-a9071cc55914', 10, 61.4, 0),
	(563, '11', 205, 'CORRECT', '0', '2026-07-20 04:23:50.856868', 'a32892a1-5ecf-4747-b24f-2dace7d8f1c3', 1, 50.5, 100),
	(564, '11', 270, 'INCORRECT', '1', '2026-07-20 04:25:50.856868', 'a32892a1-5ecf-4747-b24f-2dace7d8f1c3', 2, 81.1, 0),
	(565, '11', 260, 'CORRECT', 'def', '2026-07-20 04:27:50.856868', 'a32892a1-5ecf-4747-b24f-2dace7d8f1c3', 3, 49.9, 100),
	(566, '11', 78, 'CORRECT', '0', '2026-07-20 04:29:50.856868', 'a32892a1-5ecf-4747-b24f-2dace7d8f1c3', 4, 38.8, 100),
	(568, '11', 12, 'INCORRECT', '2', '2026-07-20 04:33:50.856868', 'a32892a1-5ecf-4747-b24f-2dace7d8f1c3', 6, 39, 0),
	(569, '11', 32, 'INCORRECT', '0', '2026-07-20 04:35:50.856868', 'a32892a1-5ecf-4747-b24f-2dace7d8f1c3', 7, 58.3, 0),
	(570, '12', 37, 'INCORRECT', '0', '2026-06-23 04:23:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 1, 106.2, 0),
	(571, '12', 201, 'INCORRECT', '1', '2026-06-23 04:25:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 2, 63.5, 0),
	(572, '12', 52, 'INCORRECT', '2', '2026-06-23 04:27:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 3, 44.5, 0),
	(573, '12', 160, 'CORRECT', '0', '2026-06-23 04:29:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 4, 24, 100),
	(574, '12', 140, 'INCORRECT', '1', '2026-06-23 04:31:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 5, 107.2, 0),
	(575, '12', 45, 'CORRECT', '0', '2026-06-23 04:33:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 6, 53.2, 100),
	(576, '12', 204, 'CORRECT', '0', '2026-06-23 04:35:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 7, 94.5, 100),
	(577, '12', 46, 'SKIP', NULL, '2026-06-23 04:37:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 8, 23.7, 0),
	(578, '12', 200, 'CORRECT', '0', '2026-06-23 04:39:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 9, 66.5, 100),
	(579, '12', 39, 'INCORRECT', '3', '2026-06-23 04:41:51.128294', '8e0701e5-6483-45d2-9b99-046394e8094d', 10, 94.1, 0),
	(580, '12', 17, 'CORRECT', '2', '2026-06-24 04:23:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 1, 56.8, 100),
	(581, '12', 77, 'INCORRECT', '1', '2026-06-24 04:25:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 2, 28.4, 0),
	(582, '12', 36, 'INCORRECT', '1', '2026-06-24 04:27:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 3, 74.5, 0),
	(583, '12', 79, 'INCORRECT', '2', '2026-06-24 04:29:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 4, 99.6, 0),
	(585, '12', 65, 'INCORRECT', '2', '2026-06-24 04:33:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 6, 48.9, 0),
	(586, '12', 10, 'INCORRECT', '3', '2026-06-24 04:35:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 7, 37.6, 0),
	(587, '12', 224, 'INCORRECT', '2', '2026-06-24 04:37:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 8, 38.8, 0),
	(588, '12', 68, 'INCORRECT', '3', '2026-06-24 04:39:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 9, 86.1, 0),
	(589, '12', 156, 'SKIP', NULL, '2026-06-24 04:41:51.128294', '774c5a54-078e-440e-907f-487efee6e16a', 10, 51.1, 0),
	(590, '12', 99, 'INCORRECT', '1', '2026-06-25 04:23:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 1, 41.1, 0),
	(591, '12', 55, 'INCORRECT', '3', '2026-06-25 04:25:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 2, 77.5, 0),
	(592, '12', 71, 'INCORRECT', '0', '2026-06-25 04:27:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 3, 48.6, 0),
	(593, '12', 44, 'INCORRECT', '0', '2026-06-25 04:29:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 4, 109.5, 0),
	(594, '12', 192, 'INCORRECT', '2', '2026-06-25 04:31:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 5, 59, 0),
	(595, '12', 176, 'INCORRECT', '2', '2026-06-25 04:33:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 6, 80.9, 0),
	(596, '12', 274, 'CORRECT', '3', '2026-06-25 04:35:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 7, 48.1, 100),
	(597, '12', 59, 'INCORRECT', '0', '2026-06-25 04:37:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 8, 99.3, 0),
	(598, '12', 35, 'CORRECT', '2', '2026-06-25 04:39:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 9, 78.4, 100),
	(599, '12', 78, 'CORRECT', '0', '2026-06-25 04:41:51.128294', 'a36c6bad-4bde-4251-a47a-0ea8c1474053', 10, 9, 100),
	(600, '12', 34, 'INCORRECT', '3', '2026-06-26 04:23:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 1, 67.7, 0),
	(602, '12', 67, 'CORRECT', '0', '2026-06-26 04:27:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 3, 66.8, 100),
	(603, '12', 208, 'INCORRECT', '2', '2026-06-26 04:29:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 4, 68.7, 0),
	(604, '12', 73, 'INCORRECT', '0', '2026-06-26 04:31:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 5, 61, 0),
	(605, '12', 267, 'INCORRECT', '0', '2026-06-26 04:33:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 6, 71.2, 0),
	(606, '12', 16, 'SKIP', NULL, '2026-06-26 04:35:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 7, 49.2, 0),
	(607, '12', 66, 'CORRECT', '0', '2026-06-26 04:37:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 8, 57, 100),
	(608, '12', 104, 'INCORRECT', '1', '2026-06-26 04:39:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 9, 64.4, 0),
	(609, '12', 127, 'CORRECT', '0', '2026-06-26 04:41:51.128294', '3f9cf661-4e99-4675-97b1-b61da4a84b1c', 10, 77.4, 100),
	(610, '12', 190, 'CORRECT', '0', '2026-06-27 04:23:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 1, 55.3, 100),
	(611, '12', 174, 'INCORRECT', '2', '2026-06-27 04:25:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 2, 37, 0),
	(612, '12', 42, 'INCORRECT', '2', '2026-06-27 04:27:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 3, 53.7, 0),
	(613, '12', 87, 'CORRECT', '0', '2026-06-27 04:29:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 4, 72.2, 100),
	(614, '12', 137, 'INCORRECT', '3', '2026-06-27 04:31:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 5, 61.9, 0),
	(615, '12', 29, 'INCORRECT', '0', '2026-06-27 04:33:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 6, 88.5, 0),
	(616, '12', 259, 'INCORRECT', '2', '2026-06-27 04:35:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 7, 46.2, 0),
	(617, '12', 48, 'INCORRECT', '0', '2026-06-27 04:37:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 8, 34, 0),
	(618, '12', 47, 'CORRECT', '3', '2026-06-27 04:39:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 9, 26.5, 100),
	(619, '12', 86, 'INCORRECT', '3', '2026-06-27 04:41:51.128294', 'c04cfd12-704b-4e1e-9d22-12b3e6f8c52c', 10, 88.2, 0),
	(620, '12', 13, 'CORRECT', '0', '2026-06-28 04:23:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 1, 39.9, 100),
	(621, '12', 27, 'CORRECT', '1', '2026-06-28 04:25:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 2, 30.7, 100),
	(622, '12', 74, 'CORRECT', '1', '2026-06-28 04:27:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 3, 25.1, 100),
	(623, '12', 15, 'INCORRECT', '2', '2026-06-28 04:29:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 4, 63.5, 0),
	(624, '12', 61, 'INCORRECT', '0', '2026-06-28 04:31:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 5, 51.7, 0),
	(625, '12', 142, 'CORRECT', '0', '2026-06-28 04:33:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 6, 61.1, 100),
	(626, '12', 152, 'CORRECT', '1', '2026-06-28 04:35:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 7, 64.6, 100),
	(627, '12', 57, 'CORRECT', '1', '2026-06-28 04:37:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 8, 62.1, 100),
	(628, '12', 32, 'INCORRECT', '3', '2026-06-28 04:39:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 9, 107.5, 0),
	(629, '12', 154, 'CORRECT', '0', '2026-06-28 04:41:51.128294', '9cddb0ce-79e0-4694-a929-e10aee88e063', 10, 69.8, 100),
	(630, '12', 161, 'CORRECT', '0', '2026-06-29 04:23:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 1, 39.2, 100),
	(631, '12', 60, 'INCORRECT', '3', '2026-06-29 04:25:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 2, 37.9, 0),
	(632, '12', 54, 'INCORRECT', '0', '2026-06-29 04:27:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 3, 96.8, 0),
	(633, '12', 119, 'INCORRECT', '3', '2026-06-29 04:29:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 4, 73.5, 0),
	(634, '12', 109, 'SKIP', NULL, '2026-06-29 04:31:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 5, 50.1, 0),
	(636, '12', 72, 'INCORRECT', '2', '2026-06-29 04:35:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 7, 69.4, 0),
	(638, '12', 80, 'CORRECT', '3', '2026-06-29 04:39:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 9, 62.4, 100),
	(639, '12', 43, 'INCORRECT', '0', '2026-06-29 04:41:51.128294', 'd82bc375-fd2d-41f6-969d-61e49aadd51b', 10, 89.2, 0),
	(640, '12', 11, 'CORRECT', '1', '2026-06-30 04:23:51.128294', 'b609f374-9f99-4e99-bcdd-eb17c3be8c77', 1, 67.7, 100),
	(641, '12', 58, 'INCORRECT', '3', '2026-06-30 04:25:51.128294', 'b609f374-9f99-4e99-bcdd-eb17c3be8c77', 2, 96.3, 0),
	(642, '12', 53, 'CORRECT', '0', '2026-06-30 04:27:51.128294', 'b609f374-9f99-4e99-bcdd-eb17c3be8c77', 3, 51.2, 100),
	(643, '12', 31, 'CORRECT', '1', '2026-06-30 04:29:51.128294', 'b609f374-9f99-4e99-bcdd-eb17c3be8c77', 4, 78, 100),
	(644, '12', 62, 'INCORRECT', '3', '2026-06-30 04:31:51.128294', 'b609f374-9f99-4e99-bcdd-eb17c3be8c77', 5, 50.9, 0),
	(645, '13', 31, 'CORRECT', '1', '2026-07-21 04:23:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 1, 39.1, 100),
	(646, '13', 87, 'INCORRECT', '2', '2026-07-21 04:25:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 2, 59.8, 0),
	(647, '13', 37, 'SKIP', NULL, '2026-07-21 04:27:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 3, 86.9, 0),
	(648, '13', 54, 'INCORRECT', '1', '2026-07-21 04:29:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 4, 97.2, 0);
INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(649, '13', 248, 'INCORRECT', '3', '2026-07-21 04:31:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 5, 50.1, 0),
	(650, '13', 14, 'INCORRECT', '3', '2026-07-21 04:33:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 6, 74.5, 0),
	(651, '13', 28, 'CORRECT', '0', '2026-07-21 04:35:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 7, 75.6, 100),
	(652, '13', 105, 'INCORRECT', '1', '2026-07-21 04:37:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 8, 29.6, 0),
	(653, '13', 109, 'INCORRECT', '1', '2026-07-21 04:39:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 9, 87.6, 0),
	(654, '13', 242, 'SKIP', NULL, '2026-07-21 04:41:51.41577', 'd7002106-4e6e-4552-a283-443bbd3bbb8f', 10, 39.5, 0),
	(655, '13', 79, 'CORRECT', '1', '2026-07-22 04:23:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 1, 68.9, 100),
	(656, '13', 267, 'INCORRECT', '0', '2026-07-22 04:25:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 2, 84.7, 0),
	(657, '13', 64, 'INCORRECT', '3', '2026-07-22 04:27:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 3, 72.5, 0),
	(658, '13', 23, 'INCORRECT', '3', '2026-07-22 04:29:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 4, 84.3, 0),
	(659, '13', 176, 'INCORRECT', '2', '2026-07-22 04:31:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 5, 92.7, 0),
	(660, '13', 165, 'INCORRECT', '2', '2026-07-22 04:33:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 6, 47.8, 0),
	(661, '13', 33, 'CORRECT', '0', '2026-07-22 04:35:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 7, 85, 100),
	(662, '13', 60, 'INCORRECT', '1', '2026-07-22 04:37:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 8, 31.3, 0),
	(663, '13', 72, 'INCORRECT', '0', '2026-07-22 04:39:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 9, 89.5, 0),
	(664, '13', 29, 'INCORRECT', '0', '2026-07-22 04:41:51.41577', '9320011d-7013-43cf-bc20-78066b012a14', 10, 52.9, 0),
	(665, '13', 26, 'INCORRECT', '2', '2026-07-23 04:23:51.41577', '26f55756-b0fd-4cf1-8572-9f5a3d645430', 1, 34.9, 0),
	(666, '13', 255, 'INCORRECT', '2', '2026-07-23 04:25:51.41577', '26f55756-b0fd-4cf1-8572-9f5a3d645430', 2, 63.8, 0),
	(668, '13', 75, 'INCORRECT', '3', '2026-07-23 04:29:51.41577', '26f55756-b0fd-4cf1-8572-9f5a3d645430', 4, 68.5, 0),
	(669, '13', 243, 'INCORRECT', '3', '2026-07-23 04:31:51.41577', '26f55756-b0fd-4cf1-8572-9f5a3d645430', 5, 37.4, 0),
	(670, '13', 190, 'CORRECT', '0', '2026-07-23 04:33:51.41577', '26f55756-b0fd-4cf1-8572-9f5a3d645430', 6, 60.6, 100),
	(671, '13', 146, 'INCORRECT', '3', '2026-07-23 04:35:51.41577', '26f55756-b0fd-4cf1-8572-9f5a3d645430', 7, 17.2, 0),
	(674, '13', 20, 'CORRECT', '3', '2026-07-23 04:41:51.41577', '26f55756-b0fd-4cf1-8572-9f5a3d645430', 10, 54.7, 100),
	(675, '13', 182, 'INCORRECT', '1', '2026-07-24 04:23:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 1, 25.8, 0),
	(676, '13', 119, 'INCORRECT', '1', '2026-07-24 04:25:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 2, 53.5, 0),
	(677, '13', 42, 'CORRECT', '1', '2026-07-24 04:27:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 3, 34.4, 100),
	(678, '13', 49, 'INCORRECT', '0', '2026-07-24 04:29:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 4, 34.1, 0),
	(679, '13', 126, 'CORRECT', '3', '2026-07-24 04:31:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 5, 71.9, 100),
	(680, '13', 24, 'INCORRECT', '1', '2026-07-24 04:33:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 6, 104.7, 0),
	(681, '13', 212, 'INCORRECT', '3', '2026-07-24 04:35:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 7, 80, 0),
	(682, '13', 12, 'INCORRECT', '2', '2026-07-24 04:37:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 8, 73, 0),
	(683, '13', 236, 'INCORRECT', '3', '2026-07-24 04:39:51.41577', '44d2f217-0fed-4ba1-810c-967f65696644', 9, 73, 0),
	(685, '13', 272, 'CORRECT', '1', '2026-07-25 04:23:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 1, 60, 100),
	(686, '13', 137, 'INCORRECT', '2', '2026-07-25 04:25:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 2, 86.5, 0),
	(687, '13', 80, 'INCORRECT', '1', '2026-07-25 04:27:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 3, 84.6, 0),
	(688, '13', 30, 'CORRECT', '0', '2026-07-25 04:29:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 4, 61.1, 100),
	(689, '13', 89, 'INCORRECT', '3', '2026-07-25 04:31:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 5, 42.7, 0),
	(690, '13', 220, 'INCORRECT', '3', '2026-07-25 04:33:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 6, 59.1, 0),
	(691, '13', 202, 'INCORRECT', '1', '2026-07-25 04:35:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 7, 43.2, 0),
	(692, '13', 201, 'INCORRECT', '1', '2026-07-25 04:37:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 8, 63.8, 0),
	(693, '13', 50, 'INCORRECT', '1', '2026-07-25 04:39:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 9, 26.9, 0),
	(694, '13', 38, 'SKIP', NULL, '2026-07-25 04:41:51.41577', 'c6f27d02-fb39-465a-8103-99ee1a84bd67', 10, 62.8, 0),
	(695, '13', 77, 'CORRECT', '0', '2026-07-26 04:23:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 1, 47.9, 100),
	(696, '13', 78, 'CORRECT', '0', '2026-07-26 04:25:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 2, 55.2, 100),
	(697, '13', 274, 'INCORRECT', '1', '2026-07-26 04:27:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 3, 67.7, 0),
	(698, '13', 46, 'CORRECT', '1', '2026-07-26 04:29:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 4, 36.7, 100),
	(699, '13', 59, 'INCORRECT', '0', '2026-07-26 04:31:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 5, 80.4, 0),
	(700, '13', 52, 'INCORRECT', '2', '2026-07-26 04:33:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 6, 33.1, 0),
	(701, '13', 262, 'INCORRECT', '잘못된 답변', '2026-07-26 04:35:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 7, 57.3, 0),
	(702, '13', 178, 'INCORRECT', '3', '2026-07-26 04:37:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 8, 73.8, 0),
	(703, '13', 41, 'CORRECT', '1', '2026-07-26 04:39:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 9, 57.4, 100),
	(704, '13', 22, 'INCORRECT', '1', '2026-07-26 04:41:51.41577', '5e929969-d24e-4633-b7ee-f034b08a0437', 10, 80, 0),
	(705, '13', 183, 'INCORRECT', '1', '2026-07-27 04:23:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 1, 42.4, 0),
	(706, '13', 35, 'INCORRECT', '1', '2026-07-27 04:25:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 2, 42.6, 0),
	(707, '13', 56, 'INCORRECT', '3', '2026-07-27 04:27:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 3, 81.5, 0),
	(708, '13', 73, 'INCORRECT', '1', '2026-07-27 04:29:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 4, 76.4, 0),
	(709, '13', 260, 'SKIP', NULL, '2026-07-27 04:31:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 5, 54.6, 0),
	(710, '13', 47, 'INCORRECT', '2', '2026-07-27 04:33:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 6, 66.7, 0),
	(711, '13', 25, 'INCORRECT', '2', '2026-07-27 04:35:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 7, 64.9, 0),
	(712, '13', 231, 'INCORRECT', '2', '2026-07-27 04:37:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 8, 31.5, 0),
	(713, '13', 132, 'INCORRECT', '1', '2026-07-27 04:39:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 9, 66.1, 0),
	(714, '13', 40, 'INCORRECT', '0', '2026-07-27 04:41:51.41577', '429310fc-1167-4831-89b4-c63829f06fc4', 10, 56.6, 0),
	(715, '13', 65, 'INCORRECT', '3', '2026-07-28 04:23:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 1, 47, 0),
	(716, '13', 94, 'INCORRECT', '0', '2026-07-28 04:25:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 2, 35.9, 0),
	(717, '13', 90, 'CORRECT', '0', '2026-07-28 04:27:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 3, 53.2, 100),
	(718, '13', 159, 'SKIP', NULL, '2026-07-28 04:29:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 4, 96, 0),
	(719, '13', 69, 'INCORRECT', '2', '2026-07-28 04:31:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 5, 81.4, 0),
	(720, '13', 51, 'INCORRECT', '0', '2026-07-28 04:33:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 6, 54.8, 0),
	(722, '13', 144, 'CORRECT', '0', '2026-07-28 04:37:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 8, 74.9, 100),
	(723, '13', 66, 'INCORRECT', '3', '2026-07-28 04:39:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 9, 58.8, 0),
	(724, '13', 96, 'INCORRECT', '2', '2026-07-28 04:41:51.41577', 'facb6798-bf4f-4b13-9e6c-2f48d1a3a110', 10, 30.4, 0),
	(725, '2', 216, 'CORRECT', '0', '2026-08-03 07:04:46.026645', '2bf2cbf8-3b1d-4d5f-aaff-183f19784498', 1, 8.29, 187.5),
	(726, '2', 257, 'INCORRECT', '0', '2026-08-03 07:04:46.026655', '2bf2cbf8-3b1d-4d5f-aaff-183f19784498', 2, 14.11, 0),
	(727, '2', 229, 'INCORRECT', '3', '2026-08-03 07:04:46.026661', '2bf2cbf8-3b1d-4d5f-aaff-183f19784498', 3, 8.04, 0),
	(728, '2', 269, 'INCORRECT', '3', '2026-08-03 07:04:46.026667', '2bf2cbf8-3b1d-4d5f-aaff-183f19784498', 4, 29.71, 0),
	(729, '2', 240, 'CORRECT', '3', '2026-08-03 07:04:46.026673', '2bf2cbf8-3b1d-4d5f-aaff-183f19784498', 5, 6.95, 150),
	(730, '2', 47, 'CORRECT', '3', '2026-08-03 07:50:50.996753', '6e00f5b9-97a0-492f-b437-bce67a0ace66', 1, 10.08, 125),
	(731, '2', 40, 'INCORRECT', '3', '2026-08-03 07:50:50.996772', '6e00f5b9-97a0-492f-b437-bce67a0ace66', 2, 26.42, 0),
	(732, '2', 42, 'CORRECT', '1', '2026-08-03 07:50:50.996785', '6e00f5b9-97a0-492f-b437-bce67a0ace66', 3, 7.66, 125),
	(733, '2', 46, 'CORRECT', '1', '2026-08-03 07:50:50.996799', '6e00f5b9-97a0-492f-b437-bce67a0ace66', 4, 15.92, 125),
	(734, '2', 45, 'CORRECT', '0', '2026-08-03 07:50:50.99681', '6e00f5b9-97a0-492f-b437-bce67a0ace66', 5, 11.54, 125),
	(735, '2', 59, 'CORRECT', '1', '2026-08-03 12:07:35.593187', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 1, 13.16, 187.5),
	(736, '2', 39, 'CORRECT', '1', '2026-08-03 12:07:35.593197', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 2, 8.34, 187.5),
	(737, '2', 35, 'INCORRECT', '0', '2026-08-03 12:07:35.593203', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 3, 8.06, 0),
	(738, '2', 247, 'INCORRECT', '3', '2026-08-03 12:07:35.593209', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 4, 17.57, 0),
	(739, '2', 239, 'CORRECT', '0', '2026-08-03 12:07:35.593215', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 5, 4.93, 150),
	(740, '2', 257, 'CORRECT', '3', '2026-08-03 12:07:35.593219', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 6, 4.99, 187.5),
	(741, '2', 197, 'CORRECT', '0', '2026-08-03 12:07:35.593224', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 7, 12.87, 150),
	(742, '2', 196, 'INCORRECT', '1', '2026-08-03 12:07:35.593229', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 8, 12.78, 0),
	(743, '2', 266, 'CORRECT', '0', '2026-08-03 12:07:35.593234', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 9, 52.17, 138.01),
	(744, '2', 233, 'CORRECT', '0', '2026-08-03 12:07:35.593238', '342ea4b9-9dad-4b3c-ae3b-17e299399f70', 10, 4.73, 150),
	(745, '2', 120, 'INCORRECT', '0', '2026-08-03 12:11:51.758367', '7377fc66-0bdf-4c29-a573-872f1bf67cec', 1, 12.11, 0),
	(746, '2', 96, 'CORRECT', '3', '2026-08-03 12:11:51.758371', '7377fc66-0bdf-4c29-a573-872f1bf67cec', 2, 6.72, 125),
	(747, '2', 121, 'CORRECT', '0', '2026-08-03 12:11:51.758374', '7377fc66-0bdf-4c29-a573-872f1bf67cec', 3, 3.06, 125),
	(748, '2', 70, 'CORRECT', '3', '2026-08-03 12:11:51.758376', '7377fc66-0bdf-4c29-a573-872f1bf67cec', 4, 8.13, 125),
	(749, '2', 71, 'CORRECT', '1', '2026-08-03 12:11:51.758378', '7377fc66-0bdf-4c29-a573-872f1bf67cec', 5, 5.25, 125),
	(750, '2', 120, 'CORRECT', '3', '2026-08-03 12:12:32.529749', '2d9520e6-912e-4b29-9ab3-8ab1919b7559', 1, 3.08, 125),
	(751, '2', 196, 'CORRECT', '0', '2026-08-04 07:36:37.432043', 'e5eb6f34-f312-407f-8d55-064d2d306855', 1, 7.693, 150),
	(752, '2', 247, 'CORRECT', '0', '2026-08-04 07:42:18.699607', '6049b21d-464d-41f6-a29f-1eb23d0d5c34', 1, 2.79, 150),
	(753, '2', 269, 'INCORRECT', '0', '2026-08-04 10:19:39.335688', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 1, 4.34, 0);
INSERT INTO public.user_progress (id, user_id, question_id, is_correct, user_answer, attempted_at, session_id, sequence_number, elapsed_seconds, achievement_score) VALUES
	(754, '2', 33, 'CORRECT', '0', '2026-08-04 10:19:39.335693', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 2, 24.97, 150),
	(755, '2', 63, 'INCORRECT', '0', '2026-08-04 10:19:39.335695', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 3, 1.96, 0),
	(756, '2', 64, 'CORRECT', '2', '2026-08-04 10:19:39.335698', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 4, 6.67, 150),
	(757, '2', 22, 'CORRECT', '0', '2026-08-04 10:19:39.3357', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 5, 2.39, 150),
	(758, '2', 38, 'CORRECT', '1', '2026-08-04 10:19:39.335701', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 6, 2.02, 150),
	(759, '2', 187, 'INCORRECT', '2', '2026-08-04 10:19:39.335703', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 7, 1.79, 0),
	(760, '2', 248, 'INCORRECT', '1', '2026-08-04 10:19:39.335705', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 8, 1.71, 0),
	(761, '2', 192, 'INCORRECT', '3', '2026-08-04 10:19:39.335706', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 9, 8.96, 0),
	(762, '2', 241, 'CORRECT', '0', '2026-08-04 10:19:39.335708', '3d3815e6-52ba-4ad4-ac1c-b14863cd0b17', 10, 5.7, 125);


--
-- Name: code_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.code_files_id_seq', 2, true);


--
-- Name: excel_questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.excel_questions_id_seq', 2, true);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.questions_id_seq', 277, true);


--
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.subjects_id_seq', 5, true);


--
-- Name: user_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_progress_id_seq', 762, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 13, true);


--
-- PostgreSQL database dump complete
--

\unrestrict EzLu7cDFoqO8hf7qqbthqWUTynWAKyM4s3flsHYB3OZYORjEvSu6hDza8KuhUiB

