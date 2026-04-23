class Category {
  final String id;
  final String name;
  final String emoji;
  final String description;
  final List<String> storyIds;

  Category({
    required this.id,
    required this.name,
    required this.emoji,
    required this.description,
    required this.storyIds,
  });

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id'] as String,
      name: json['name'] as String,
      emoji: json['emoji'] as String,
      description: json['description'] as String,
      storyIds: List<String>.from(json['storyIds'] as List),
    );
  }
}
