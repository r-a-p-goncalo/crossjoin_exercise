import re


THREAD_CATEGORY_PATTERNS = [

    # JVM Internal
    (r"^Reference Handler$", "JVM Internal"),
    (r"^Finalizer$", "JVM Internal"),
    (r"^Signal Dispatcher$", "JVM Internal"),
    (r"^Service Thread$", "JVM Internal"),
    (r"^C\d+ CompilerThread\d+$", "JVM Internal"),
    (r"^Sweeper thread$", "JVM Internal"),
    (r"^Common-Cleaner$", "JVM Internal"),
    (r"^DestroyJavaVM$", "JVM Internal"),
    (r"^VM Thread$", "JVM Internal"),
    (r"^VM Periodic Task Thread$", "JVM Internal"),
    (r"^Attach Listener$", "JVM Internal"),

    # Garbage Collector
    (r"^GC Thread#\d+$", "Garbage Collector"),
    (r"^G1 Main Marker$", "Garbage Collector"),
    (r"^G1 Conc#\d+$", "Garbage Collector"),
    (r"^G1 Refine#\d+$", "Garbage Collector"),
    (r"^G1 Young RemSet Sampling$", "Garbage Collector"),

    # Tomcat
    (r"^http-nio-\d+-Acceptor$", "Tomcat"),
    (r"^http-nio-\d+-ClientPoller$", "Tomcat"),
    (r"^http-nio-\d+-BlockPoller$", "Tomcat"),
    (r"^http-nio-\d+-exec-\d+$", "Tomcat"),
    (r"^Catalina-utility-\d+$", "Tomcat"),

    # Spring
    (r"^spring\.cloud\.inetutils$", "Spring"),

    # Application
    (r"^container-\d+$", "Application"),
    (r"^pool-\d+-thread-\d+$", "Application"),
    (r"^AsynchThread-\d+$", "Application"),

    # Redis
    (r"^lettuce-.*", "Redis"),
    (r"^LLEN.*Reader$", "Redis"),
    (r"^LLEN.*Writer$", "Redis"),

    # Commons Pool
    (r"^commons-pool-evictor-thread$", "Connection Pool"),

    # RabbitMQ / AMQP
    (r"^AMQP Connection.*", "AMQP"),

    # Jaeger
    (r"^jaeger\.RemoteReporter.*QueueProcessor$", "Jaeger"),
    (r"^jaeger\.RemoteReporter.*FlushTimer$", "Jaeger"),
]

CUSTOM_CALL_PREFIXES = (
    "com.crossjoin",
    "pt.crossjoin",
    "com.company",
     "com.crossjointest."
)


def is_custom_call(function_name: str) -> bool:
    """
    Returns True if any package, class or method component
    contains the word 'tuxedo' (case-insensitive).
    """

    return function_name.startswith(CUSTOM_CALL_PREFIXES) or any(
        "tuxedo" in part.lower()
        for part in function_name.split(".")
    )


def get_thread_category_from_name(thread_name: str) -> str:
    if thread_name is None:
        return None

    for pattern, category in THREAD_CATEGORY_PATTERNS:
        if re.match(pattern, thread_name):
            return category

    return thread_name