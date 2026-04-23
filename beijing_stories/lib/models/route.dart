class RouteModel {
  final String id;
  final String name;
  final String description;
  final String coverImage;
  final List<String> storyIds;
  final int duration; // 分钟
  final int totalStories;
  final int completedStories;

  RouteModel({
    required this.id,
    required this.name,
    required this.description,
    required this.coverImage,
    required this.storyIds,
    required this.duration,
    required this.totalStories,
    this.completedStories = 0,
  });

  factory RouteModel.fromJson(Map<String, dynamic> json) {
    return RouteModel(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String,
      coverImage: json['coverImage'] as String,
      storyIds: List<String>.from(json['storyIds'] as List),
      duration: json['duration'] as int,
      totalStories: json['totalStories'] as int,
      completedStories: json['completedStories'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'coverImage': coverImage,
      'storyIds': storyIds,
      'duration': duration,
      'totalStories': totalStories,
      'completedStories': completedStories,
    };
  }

  double get progress => totalStories > 0 ? completedStories / totalStories : 0;
}
