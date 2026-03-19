// main.cpp
// Single-file C++17 Qt Widgets program implementing the Student Management System GUI
// Save as main.cpp
//
// Compile (Qt5 example on Linux with pkg-config):
//   g++ main.cpp -fPIC $(pkg-config --cflags --libs Qt5Widgets) -o StudentManagement
//
// Compile (Qt6, if pkg-config name is Qt6Widgets):
//   g++ main.cpp -fPIC $(pkg-config --cflags --libs Qt6Widgets) -o StudentManagement
//
// Or use Qt Creator / qmake / CMake. This file uses Q_OBJECT and includes "main.moc"
// so it builds in a single-file setup when moc is run automatically by your build system.
//
// Run:
//   ./StudentManagement

#include <QtWidgets>

class StudentManagementWidget : public QWidget {
    Q_OBJECT

public:
    StudentManagementWidget(QWidget *parent = nullptr) : QWidget(parent) {
        setupUi();
        setupConnections();
        populateInitialData();
    }

private:
    QLineEdit *nameEdit;
    QLineEdit *ageEdit;
    QLineEdit *emailEdit;
    QLineEdit *courseEdit;
    QPushButton *addButton;
    QPushButton *updateButton;
    QTableWidget *table;
    int nextId = 1;

    void setupUi() {
        // Title label
        QLabel *title = new QLabel("Student Management System - GUI");
        QFont titleFont = title->font();
        titleFont.setBold(true);
        title->setFont(titleFont);
        title->setAlignment(Qt::AlignLeft);

        // Form layout
        QLabel *lblName = new QLabel("Name:");
        nameEdit = new QLineEdit();
        nameEdit->setMinimumWidth(140);

        QLabel *lblAge = new QLabel("Age:");
        ageEdit = new QLineEdit();
        ageEdit->setMaximumWidth(60);

        QLabel *lblEmail = new QLabel("Email:");
        emailEdit = new QLineEdit();
        emailEdit->setMinimumWidth(220);

        QLabel *lblCourse = new QLabel("Course:");
        courseEdit = new QLineEdit();
        courseEdit->setMaximumWidth(120);

        addButton = new QPushButton("Add");
        updateButton = new QPushButton("Update");

        QHBoxLayout *formLayout = new QHBoxLayout();
        formLayout->addWidget(lblName);
        formLayout->addWidget(nameEdit);
        formLayout->addSpacing(8);
        formLayout->addWidget(lblAge);
        formLayout->addWidget(ageEdit);
        formLayout->addSpacing(8);
        formLayout->addWidget(lblEmail);
        formLayout->addWidget(emailEdit);
        formLayout->addSpacing(8);
        formLayout->addWidget(lblCourse);
        formLayout->addWidget(courseEdit);
        formLayout->addSpacing(8);
        formLayout->addWidget(addButton);
        formLayout->addWidget(updateButton);
        formLayout->addStretch();

        // Table setup
        table = new QTableWidget();
        table->setColumnCount(5);
        QStringList headers = {"ID", "Name", "Age", "Email", "Course"};
        table->setHorizontalHeaderLabels(headers);
        table->horizontalHeader()->setSectionResizeMode(0, QHeaderView::ResizeToContents);
        table->horizontalHeader()->setSectionResizeMode(1, QHeaderView::Stretch);
        table->horizontalHeader()->setSectionResizeMode(2, QHeaderView::ResizeToContents);
        table->horizontalHeader()->setSectionResizeMode(3, QHeaderView::Stretch);
        table->horizontalHeader()->setSectionResizeMode(4, QHeaderView::ResizeToContents);
        table->setSelectionBehavior(QAbstractItemView::SelectRows);
        table->setEditTriggers(QAbstractItemView::NoEditTriggers);
        table->setAlternatingRowColors(true);

        // Layout
        QVBoxLayout *main = new QVBoxLayout(this);
        main->addWidget(title);
        main->addSpacing(6);
        main->addLayout(formLayout);
        main->addSpacing(6);
        main->addWidget(table);

        setWindowTitle("Student Management System - GUI");
        resize(900, 520);
    }

    void setupConnections() {
        connect(addButton, &QPushButton::clicked, this, &StudentManagementWidget::onAddClicked);
        connect(updateButton, &QPushButton::clicked, this, &StudentManagementWidget::onUpdateClicked);
        connect(table, &QTableWidget::itemSelectionChanged, this, &StudentManagementWidget::onTableSelectionChanged);
    }

    void populateInitialData() {
        // initial rows matching the screenshot
        addRow("vansh", "20", "vansh@gmail.com", "Btech");
        addRow("aman",  "21", "aman@gmail.com",  "Mtech");
        addRow("kunal", "22", "kunal@gmail.com", "MCA");
    }

    void addRow(const QString &name, const QString &age, const QString &email, const QString &course) {
        int row = table->rowCount();
        table->insertRow(row);
        table->setItem(row, 0, new QTableWidgetItem(QString::number(nextId++)));
        table->setItem(row, 1, new QTableWidgetItem(name));
        table->setItem(row, 2, new QTableWidgetItem(age));
        table->setItem(row, 3, new QTableWidgetItem(email));
        table->setItem(row, 4, new QTableWidgetItem(course));
    }

private slots:
    void onAddClicked() {
        QString name = nameEdit->text().trimmed();
        QString age  = ageEdit->text().trimmed();
        QString email = emailEdit->text().trimmed();
        QString course = courseEdit->text().trimmed();

        if (name.isEmpty()) {
            QMessageBox::warning(this, "Validation", "Please enter a name.");
            return;
        }

        addRow(name, age, email, course);

        // Clear inputs after adding
        nameEdit->clear();
        ageEdit->clear();
        emailEdit->clear();
        courseEdit->clear();
    }

    void onUpdateClicked() {
        QList<QTableWidgetSelectionRange> ranges = table->selectedRanges();
        if (ranges.isEmpty()) {
            QMessageBox::information(this, "Update", "Please select a row to update.");
            return;
        }

        int row = ranges.first().topRow();

        QString name = nameEdit->text().trimmed();
        QString age  = ageEdit->text().trimmed();
        QString email = emailEdit->text().trimmed();
        QString course = courseEdit->text().trimmed();

        // Update only non-empty fields (keeps old values if field left blank)
        if (!name.isEmpty())  table->item(row, 1)->setText(name);
        if (!age.isEmpty())   table->item(row, 2)->setText(age);
        if (!email.isEmpty()) table->item(row, 3)->setText(email);
        if (!course.isEmpty()) table->item(row, 4)->setText(course);

        // Clear inputs after update
        nameEdit->clear();
        ageEdit->clear();
        emailEdit->clear();
        courseEdit->clear();
    }

    void onTableSelectionChanged() {
        QList<QTableWidgetSelectionRange> ranges = table->selectedRanges();
        if (ranges.isEmpty()) {
            nameEdit->clear();
            ageEdit->clear();
            emailEdit->clear();
            courseEdit->clear();
            return;
        }
        int row = ranges.first().topRow();
        // Guard: items may be null if table is empty, but not expected here
        if (table->item(row,1)) nameEdit->setText(table->item(row,1)->text());
        if (table->item(row,2)) ageEdit->setText(table->item(row,2)->text());
        if (table->item(row,3)) emailEdit->setText(table->item(row,3)->text());
        if (table->item(row,4)) courseEdit->setText(table->item(row,4)->text());
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    StudentManagementWidget w;
    w.show();
    return app.exec();
}

#include "main.moc"
